#
# This file is part of the linuxpy project
#
# Copyright (c) 2023 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

"""Human friendly functional interface to V4L2 (Video 4 Linux 2) subsystem."""

import asyncio
import collections
import contextlib
import copy
import ctypes
import enum
import errno
import fractions
import logging
import mmap
import os
import select
import time
from collections import UserDict
from pathlib import Path

from linuxpy.ctypes import cast, cenum, create_string_buffer, memcpy, string_at
from linuxpy.device import (
    BaseDevice,
    ReentrantOpen,
    iter_device_files,
)
from linuxpy.io import IO
from linuxpy.ioctl import ioctl
from linuxpy.types import AsyncIterator, Buffer, Callable, Iterable, Iterator, Optional, PathLike, Self
from linuxpy.util import astream, bit_indexes, make_find

from . import raw

log = logging.getLogger(__name__)
log_mmap = log.getChild("mmap")


class V4L2Error(Exception):
    """Video for linux 2 error"""


def _enum(name, prefix, klass=enum.IntEnum):
    return klass(
        name,
        ((name.replace(prefix, ""), getattr(raw, name)) for name in dir(raw) if name.startswith(prefix)),
    )


FrameSizeType = raw.Frmsizetypes
FrameIntervalType = raw.Frmivaltypes
Field = raw.Field
ImageFormatFlag = raw.ImageFormatFlag
Capability = raw.Capability
ControlID = raw.ControlID
ControlFlag = raw.ControlFlag
ControlType = raw.CtrlType
ControlClass = raw.ControlClass
SelectionTarget = raw.SelectionTarget
EventType = raw.EventType
IOC = raw.IOC
BufferType = raw.BufType
BufferFlag = raw.BufferFlag
InputType = raw.InputType
PixelFormat = raw.PixelFormat
MetaFormat = raw.MetaFormat
FrameSizeType = raw.Frmsizetypes
Memory = raw.Memory
InputStatus = raw.InputStatus
OutputType = raw.OutputType
InputCapabilities = raw.InputCapabilities
OutputCapabilities = raw.OutputCapabilities
Priority = raw.Priority
TimeCodeType = raw.TimeCodeType
TimeCodeFlag = raw.TimeCodeFlag
EventSubscriptionFlag = raw.EventSubscriptionFlag
StandardID = raw.StandardID


def V4L2_CTRL_ID2CLASS(id_):
    return id_ & 0x0FFF0000  # unsigned long


def human_pixel_format(ifmt):
    return "".join(map(chr, ((ifmt >> i) & 0xFF for i in range(0, 4 * 8, 8))))


PixelFormat.human_str = lambda self: human_pixel_format(self.value)
MetaFormat.human_str = lambda self: human_pixel_format(self.value)


Info = collections.namedtuple(
    "Info",
    "driver card bus_info version capabilities device_capabilities "
    "crop_capabilities buffers formats frame_sizes inputs outputs controls",
)

ImageFormat = collections.namedtuple("ImageFormat", "type description flags pixel_format")

MetaFmt = collections.namedtuple("MetaFmt", "format max_buffer_size width height bytes_per_line")

Format = collections.namedtuple("Format", "width height pixel_format size")

CropCapability = collections.namedtuple("CropCapability", "type bounds defrect pixel_aspect")

Rect = collections.namedtuple("Rect", "left top width height")

Size = collections.namedtuple("Size", "width height")

FrameType = collections.namedtuple("FrameType", "type pixel_format width height min_fps max_fps step_fps")

Input = collections.namedtuple("InputType", "index name type audioset tuner std status capabilities")

Output = collections.namedtuple("OutputType", "index name type audioset modulator std capabilities")

Standard = collections.namedtuple("Standard", "index id name frameperiod framelines")


INFO_REPR = """\
driver = {info.driver}
card = {info.card}
bus = {info.bus_info}
version = {info.version}
capabilities = {capabilities}
device_capabilities = {device_capabilities}
buffers = {buffers}
"""


def mem_map(fd, length, offset):
    log_mmap.debug("%s, length=%d, offset=%d", fd, length, offset)
    return mmap.mmap(fd, length, offset=offset)


def flag_items(flag):
    return [item for item in type(flag) if item in flag]


def Info_repr(info):
    dcaps = "|".join(cap.name for cap in flag_items(info.device_capabilities))
    caps = "|".join(cap.name for cap in flag_items(info.capabilities))
    buffers = "|".join(buff.name for buff in info.buffers)
    return INFO_REPR.format(info=info, capabilities=caps, device_capabilities=dcaps, buffers=buffers)


Info.__repr__ = Info_repr


def raw_crop_caps_to_crop_caps(crop):
    return CropCapability(
        type=BufferType(crop.type),
        bounds=Rect(
            crop.bounds.left,
            crop.bounds.top,
            crop.bounds.width,
            crop.bounds.height,
        ),
        defrect=Rect(
            crop.defrect.left,
            crop.defrect.top,
            crop.defrect.width,
            crop.defrect.height,
        ),
        pixel_aspect=crop.pixelaspect.numerator / crop.pixelaspect.denominator,
    )


CropCapability.from_raw = raw_crop_caps_to_crop_caps


def read_crop_capabilities(fd, buffer_type: BufferType) -> raw.v4l2_cropcap:
    crop = raw.v4l2_cropcap()
    crop.type = buffer_type
    return ioctl(fd, IOC.CROPCAP, crop)


def iter_read(fd, ioc, indexed_struct, start=0, stop=128, step=1, ignore_einval=False):
    for index in range(start, stop, step):
        indexed_struct.index = index
        try:
            ioctl(fd, ioc, indexed_struct)
            yield indexed_struct
        except OSError as error:
            if error.errno == errno.EINVAL:
                if ignore_einval:
                    continue
                else:
                    break
            elif error.errno == errno.ENOTTY:
                # The ioctl is not supported by the driver
                break
            elif error.errno == errno.ENODATA:
                break
            else:
                raise


def iter_read_frame_intervals(fd, fmt, w, h):
    value = raw.v4l2_frmivalenum()
    value.pixel_format = fmt
    value.width = w
    value.height = h
    count = 0
    for val in iter_read(fd, IOC.ENUM_FRAMEINTERVALS, value):
        # values come in frame interval (fps = 1/interval)
        try:
            ftype = FrameIntervalType(val.type)
        except ValueError:
            break
        if ftype == FrameIntervalType.DISCRETE:
            min_fps = max_fps = step_fps = fractions.Fraction(val.discrete.denominator / val.discrete.numerator)
        else:
            if val.stepwise.min.numerator == 0:
                min_fps = 0
            else:
                min_fps = fractions.Fraction(val.stepwise.min.denominator, val.stepwise.min.numerator)
            if val.stepwise.max.numerator == 0:
                max_fps = 0
            else:
                max_fps = fractions.Fraction(val.stepwise.max.denominator, val.stepwise.max.numerator)
            if val.stepwise.step.numerator == 0:
                step_fps = 0
            else:
                step_fps = fractions.Fraction(val.stepwise.step.denominator, val.stepwise.step.numerator)
        yield FrameType(
            type=ftype,
            pixel_format=fmt,
            width=w,
            height=h,
            min_fps=min_fps,
            max_fps=max_fps,
            step_fps=step_fps,
        )
        count += 1
    if not count:
        # If it wasn't possible to get frame interval, report discovered frame size anyway
        yield FrameType(
            type=FrameIntervalType.DISCRETE,
            pixel_format=fmt,
            width=w,
            height=h,
            min_fps=0,
            max_fps=0,
            step_fps=0,
        )


def frame_sizes(fd, pixel_formats):
    size = raw.v4l2_frmsizeenum()
    sizes = []
    for pixel_format in pixel_formats:
        size.pixel_format = pixel_format
        size.index = 0
        while True:
            try:
                ioctl(fd, IOC.ENUM_FRAMESIZES, size)
            except OSError:
                break
            if size.type == FrameSizeType.DISCRETE:
                sizes += iter_read_frame_intervals(fd, pixel_format, size.discrete.width, size.discrete.height)
            size.index += 1
    return sizes


def read_capabilities(fd):
    caps = raw.v4l2_capability()
    ioctl(fd, IOC.QUERYCAP, caps)
    return caps


def iter_read_formats(fd, type):
    format = raw.v4l2_fmtdesc()
    format.type = type
    pixel_formats = set(PixelFormat)
    meta_formats = set(MetaFormat)
    for fmt in iter_read(fd, IOC.ENUM_FMT, format):
        pixel_fmt = fmt.pixelformat
        if type in {BufferType.VIDEO_CAPTURE, BufferType.VIDEO_OUTPUT}:
            if pixel_fmt not in pixel_formats:
                log.warning(
                    "ignored unknown pixel format %s (%d)",
                    human_pixel_format(pixel_fmt),
                    pixel_fmt,
                )
                continue
            pixel_format = PixelFormat(pixel_fmt)
        elif type in {BufferType.META_CAPTURE, BufferType.META_OUTPUT}:
            if pixel_fmt not in meta_formats:
                log.warning(
                    "ignored unknown meta format %s (%d)",
                    human_pixel_format(pixel_fmt),
                    pixel_fmt,
                )
                continue
            pixel_format = MetaFormat(pixel_fmt)
        image_format = ImageFormat(
            type=type,
            flags=ImageFormatFlag(fmt.flags),
            description=fmt.description.decode(),
            pixel_format=pixel_format,
        )
        yield image_format


def iter_read_inputs(fd):
    input = raw.v4l2_input()
    for inp in iter_read(fd, IOC.ENUMINPUT, input):
        input_type = Input(
            index=inp.index,
            name=inp.name.decode(),
            type=InputType(inp.type),
            audioset=bit_indexes(inp.audioset),
            tuner=inp.tuner,
            std=StandardID(inp.std),
            status=InputStatus(inp.status),
            capabilities=InputCapabilities(inp.capabilities),
        )
        yield input_type


def iter_read_outputs(fd):
    output = raw.v4l2_output()
    for out in iter_read(fd, IOC.ENUMOUTPUT, output):
        output_type = Output(
            index=out.index,
            name=out.name.decode(),
            type=OutputType(out.type),
            audioset=bit_indexes(out.audioset),
            modulator=out.modulator,
            std=StandardID(out.std),
            capabilities=OutputCapabilities(out.capabilities),
        )
        yield output_type


def iter_read_video_standards(fd):
    std = raw.v4l2_standard()
    for item in iter_read(fd, IOC.ENUMSTD, std):
        period = item.frameperiod
        yield Standard(
            index=item.index,
            id=StandardID(item.id),
            name=item.name.decode(),
            frameperiod=fractions.Fraction(period.denominator, period.numerator),
            framelines=item.framelines,
        )


def iter_read_controls(fd):
    ctrl = raw.v4l2_query_ext_ctrl()
    nxt = ControlFlag.NEXT_CTRL | ControlFlag.NEXT_COMPOUND
    ctrl.id = nxt
    for ctrl_ext in iter_read(fd, IOC.QUERY_EXT_CTRL, ctrl):
        yield copy.deepcopy(ctrl_ext)
        ctrl_ext.id |= nxt


def iter_read_menu(fd, ctrl):
    qmenu = raw.v4l2_querymenu()
    qmenu.id = ctrl.id
    for menu in iter_read(
        fd,
        IOC.QUERYMENU,
        qmenu,
        start=ctrl._info.minimum,
        stop=ctrl._info.maximum + 1,
        step=ctrl._info.step,
        ignore_einval=True,
    ):
        yield copy.deepcopy(menu)


def read_info(fd):
    caps = read_capabilities(fd)
    version_tuple = (
        (caps.version & 0xFF0000) >> 16,
        (caps.version & 0x00FF00) >> 8,
        (caps.version & 0x0000FF),
    )
    version_str = ".".join(map(str, version_tuple))
    device_capabilities = Capability(caps.device_caps)
    buffers = [typ for typ in BufferType if Capability[typ.name] in device_capabilities]

    img_fmt_buffer_types = {
        BufferType.VIDEO_CAPTURE,
        BufferType.VIDEO_CAPTURE_MPLANE,
        BufferType.VIDEO_OUTPUT,
        BufferType.VIDEO_OUTPUT_MPLANE,
        BufferType.VIDEO_OVERLAY,
        BufferType.META_CAPTURE,
        BufferType.META_OUTPUT,
    } & set(buffers)

    image_formats = []
    pixel_formats = set()
    for stream_type in img_fmt_buffer_types:
        for image_format in iter_read_formats(fd, stream_type):
            image_formats.append(image_format)
            pixel_formats.add(image_format.pixel_format)

    crop = raw.v4l2_cropcap()
    crop_stream_types = {
        BufferType.VIDEO_CAPTURE,
        BufferType.VIDEO_OUTPUT,
        BufferType.VIDEO_OVERLAY,
    } & set(buffers)
    crop_caps = []
    for stream_type in crop_stream_types:
        crop.type = stream_type
        try:
            ioctl(fd, IOC.CROPCAP, crop)
        except OSError:
            continue
        crop_cap = CropCapability.from_raw(crop)
        crop_caps.append(crop_cap)

    return Info(
        driver=caps.driver.decode(),
        card=caps.card.decode(),
        bus_info=caps.bus_info.decode(),
        version=version_str,
        capabilities=Capability(caps.capabilities),
        device_capabilities=device_capabilities,
        crop_capabilities=crop_caps,
        buffers=buffers,
        formats=image_formats,
        frame_sizes=frame_sizes(fd, pixel_formats),
        inputs=list(iter_read_inputs(fd)),
        outputs=list(iter_read_outputs(fd)),
        controls=list(iter_read_controls(fd)),
    )


def query_buffer(fd, buffer_type: BufferType, memory: Memory, index: int) -> raw.v4l2_buffer:
    buff = raw.v4l2_buffer()
    buff.type = buffer_type
    buff.memory = memory
    buff.index = index
    buff.reserved = 0
    ioctl(fd, IOC.QUERYBUF, buff)
    return buff


def enqueue_buffer_raw(fd, buff: raw.v4l2_buffer) -> raw.v4l2_buffer:
    if not buff.timestamp.secs:
        buff.timestamp.set_ns()
    ioctl(fd, IOC.QBUF, buff)
    return buff


def enqueue_buffer(fd, buffer_type: BufferType, memory: Memory, size: int, index: int) -> raw.v4l2_buffer:
    buff = raw.v4l2_buffer()
    buff.type = buffer_type
    buff.memory = memory
    buff.bytesused = size
    buff.index = index
    buff.field = Field.NONE
    buff.reserved = 0
    return enqueue_buffer_raw(fd, buff)


def dequeue_buffer(fd, buffer_type: BufferType, memory: Memory) -> raw.v4l2_buffer:
    buff = raw.v4l2_buffer()
    buff.type = buffer_type
    buff.memory = memory
    buff.index = 0
    buff.reserved = 0
    ioctl(fd, IOC.DQBUF, buff)
    return buff


def request_buffers(fd, buffer_type: BufferType, memory: Memory, count: int) -> raw.v4l2_requestbuffers:
    req = raw.v4l2_requestbuffers()
    req.type = buffer_type
    req.memory = memory
    req.count = count
    ioctl(fd, IOC.REQBUFS, req)
    if not req.count:
        raise OSError("Not enough buffer memory")
    return req


def free_buffers(fd, buffer_type: BufferType, memory: Memory) -> raw.v4l2_requestbuffers:
    req = raw.v4l2_requestbuffers()
    req.type = buffer_type
    req.memory = memory
    req.count = 0
    ioctl(fd, IOC.REQBUFS, req)
    return req


def export_buffer(fd, buffer_type: BufferType, index: int) -> int:
    req = raw.v4l2_exportbuffer(type=buffer_type, index=index)
    return ioctl(fd, IOC.EXPBUF, req).fd


def create_buffers(fd, format: raw.v4l2_format, memory: Memory, count: int) -> raw.v4l2_create_buffers:
    """Create buffers for Memory Mapped or User Pointer or DMA Buffer I/O"""
    req = raw.v4l2_create_buffers()
    req.format = format
    req.memory = memory
    req.count = count
    ioctl(fd, IOC.CREATE_BUFS, req)
    if not req.count:
        raise OSError("Not enough buffer memory")
    return req


def set_raw_format(fd, fmt: raw.v4l2_format):
    return ioctl(fd, IOC.S_FMT, fmt)


def set_format(fd, buffer_type: BufferType, width: int, height: int, pixel_format: str = "MJPG"):
    fmt = raw.v4l2_format()
    if isinstance(pixel_format, str):
        pixel_format = raw.v4l2_fourcc(*pixel_format)
    fmt.type = buffer_type
    fmt.fmt.pix.pixelformat = pixel_format
    fmt.fmt.pix.field = Field.ANY
    fmt.fmt.pix.width = width
    fmt.fmt.pix.height = height
    fmt.fmt.pix.bytesperline = 0
    fmt.fmt.pix.sizeimage = 0
    return set_raw_format(fd, fmt)


def get_raw_format(fd, buffer_type) -> raw.v4l2_format:
    fmt = raw.v4l2_format()
    fmt.type = buffer_type
    ioctl(fd, IOC.G_FMT, fmt)
    return fmt


def get_format(fd, buffer_type) -> Format:
    f = get_raw_format(fd, buffer_type)
    if buffer_type in {BufferType.META_CAPTURE, BufferType.META_OUTPUT}:
        return MetaFmt(
            format=MetaFormat(f.fmt.meta.dataformat),
            max_buffer_size=f.fmt.meta.buffersize,
            width=f.fmt.meta.width,
            height=f.fmt.meta.height,
            bytes_per_line=f.fmt.meta.bytesperline,
        )
    return Format(
        width=f.fmt.pix.width,
        height=f.fmt.pix.height,
        pixel_format=PixelFormat(f.fmt.pix.pixelformat),
        size=f.fmt.pix.sizeimage,
    )


def try_raw_format(fd, fmt: raw.v4l2_format):
    ioctl(fd, IOC.TRY_FMT, fmt)


def try_format(fd, buffer_type: BufferType, width: int, height: int, pixel_format: str = "MJPG"):
    fmt = raw.v4l2_format()
    if isinstance(pixel_format, str):
        pixel_format = raw.v4l2_fourcc(*pixel_format)
    fmt.type = buffer_type
    fmt.fmt.pix.pixelformat = pixel_format
    fmt.fmt.pix.field = Field.ANY
    fmt.fmt.pix.width = width
    fmt.fmt.pix.height = height
    fmt.fmt.pix.bytesperline = 0
    fmt.fmt.pix.sizeimage = 0
    return try_raw_format(fd, fmt)


def get_parm(fd, buffer_type):
    p = raw.v4l2_streamparm()
    p.type = buffer_type
    ioctl(fd, IOC.G_PARM, p)
    return p


def set_fps(fd, buffer_type, fps):
    # v4l2 fraction is u32
    max_denominator = int(min(2**32, 2**32 / fps))
    p = raw.v4l2_streamparm()
    p.type = buffer_type
    fps = fractions.Fraction(fps).limit_denominator(max_denominator)
    if buffer_type == BufferType.VIDEO_CAPTURE:
        p.parm.capture.timeperframe.numerator = fps.denominator
        p.parm.capture.timeperframe.denominator = fps.numerator
    elif buffer_type == BufferType.VIDEO_OUTPUT:
        p.parm.output.timeperframe.numerator = fps.denominator
        p.parm.output.timeperframe.denominator = fps.numerator
    else:
        raise ValueError(f"Unsupported buffer type {buffer_type!r}")
    return ioctl(fd, IOC.S_PARM, p)


def get_fps(fd, buffer_type):
    p = get_parm(fd, buffer_type)
    if buffer_type == BufferType.VIDEO_CAPTURE:
        parm = p.parm.capture
    elif buffer_type == BufferType.VIDEO_OUTPUT:
        parm = p.parm.output
    else:
        raise ValueError(f"Unsupported buffer type {buffer_type!r}")
    return fractions.Fraction(parm.timeperframe.denominator, parm.timeperframe.numerator)


def stream_on(fd, buffer_type):
    btype = cenum(buffer_type)
    return ioctl(fd, IOC.STREAMON, btype)


def stream_off(fd, buffer_type):
    btype = cenum(buffer_type)
    return ioctl(fd, IOC.STREAMOFF, btype)


def set_selection(fd, buffer_type, target, rectangle):
    sel = raw.v4l2_selection()
    sel.type = buffer_type
    sel.target = target
    sel.r.left = rectangle.left
    sel.r.top = rectangle.top
    sel.r.width = rectangle.width
    sel.r.height = rectangle.height
    ioctl(fd, IOC.S_SELECTION, sel)


def get_selection(
    fd,
    buffer_type: BufferType,
    target: SelectionTarget = SelectionTarget.CROP_DEFAULT,
):
    sel = raw.v4l2_selection()
    sel.type = buffer_type
    sel.target = target
    ioctl(fd, IOC.G_SELECTION, sel)
    return Rect(left=sel.r.left, top=sel.r.top, width=sel.r.width, height=sel.r.height)


def get_control(fd, id):
    control = raw.v4l2_control(id)
    ioctl(fd, IOC.G_CTRL, control)
    return control.value


CTRL_TYPE_CTYPE_ARRAY = {
    ControlType.U8: ctypes.c_uint8,
    ControlType.U16: ctypes.c_uint16,
    ControlType.U32: ctypes.c_uint32,
    ControlType.INTEGER: ctypes.c_int,
    ControlType.INTEGER64: ctypes.c_int64,
}


CTRL_TYPE_CTYPE_STRUCT = {
    ControlType.AREA: raw.v4l2_area,
}


def _struct_for_ctrl_type(ctrl_type):
    ctrl_type = ControlType(ctrl_type).name.lower()
    name = f"v4l2_ctrl_{ctrl_type}"
    return getattr(raw, name)


def _field_for_control(control):
    has_payload = ControlFlag.HAS_PAYLOAD in ControlFlag(control.flags)
    if has_payload:
        if control.type == ControlType.INTEGER:
            return "p_s32"
        elif control.type == ControlType.INTEGER64:
            return "p_s64"
        elif control.type == ControlType.STRING:
            return "string"
        else:
            ctrl_name = ControlType(control.type).name.lower()
            return f"p_{ctrl_name}"
    if control.type == ControlType.INTEGER64:
        return "value64"
    return "value"


def get_ctrl_type_struct(ctrl_type):
    struct = CTRL_TYPE_CTYPE_STRUCT.get(ctrl_type)
    if struct is None:
        struct = _struct_for_ctrl_type(ctrl_type)
        CTRL_TYPE_CTYPE_STRUCT[ctrl_type] = struct
    return struct


def convert_to_ctypes_array(lst, depth, ctype):
    """Convert a list (arbitrary depth) to a ctypes array."""
    if depth == 1:
        return (ctype * len(lst))(*lst)

    # Recursive case: we need to process the sub-lists first
    sub_arrays = [convert_to_ctypes_array(sub_lst, depth - 1, ctype) for sub_lst in lst]
    array_type = len(sub_arrays) * type(sub_arrays[0])  # Create the array type
    return array_type(*sub_arrays)


def _prepare_read_control_value(control: raw.v4l2_query_ext_ctrl, raw_control: raw.v4l2_ext_control):
    raw_control.id = control.id
    has_payload = ControlFlag.HAS_PAYLOAD in ControlFlag(control.flags)
    if has_payload:
        if control.type == ControlType.STRING:
            size = control.maximum + 1
            payload = ctypes.create_string_buffer(size)
            raw_control.string = payload
            raw_control.size = size
        else:
            ctype = CTRL_TYPE_CTYPE_ARRAY.get(control.type)
            raw_control.size = control.elem_size * control.elems
            if ctype is None:
                ctype = get_ctrl_type_struct(control.type)
                payload = ctype()
                raw_control.ptr = ctypes.cast(ctypes.pointer(payload), ctypes.c_void_p)
            else:
                for i in range(control.nr_of_dims):
                    ctype *= control.dims[i]
                payload = ctype()
                raw_control.size = control.elem_size * control.elems
                raw_control.ptr = ctypes.cast(payload, ctypes.c_void_p)
        return payload


def _get_control_value(control: raw.v4l2_query_ext_ctrl, raw_control: raw.v4l2_ext_control, data):
    if data is None:
        if control.type == ControlType.INTEGER64:
            return raw_control.value64
        return raw_control.value
    else:
        if control.type == ControlType.STRING:
            return data.value.decode()
        return data


def get_controls_values(fd, controls: list[raw.v4l2_query_ext_ctrl], which=raw.ControlWhichValue.CUR_VAL, request_fd=0):
    n = len(controls)
    ctrls = raw.v4l2_ext_controls()
    ctrls.which = which
    ctrls.count = n
    ctrls.request_fd = request_fd
    ctrls.controls = (n * raw.v4l2_ext_control)()
    values = [_prepare_read_control_value(*args) for args in zip(controls, ctrls.controls)]
    ioctl(fd, IOC.G_EXT_CTRLS, ctrls)
    return [_get_control_value(*args) for args in zip(controls, ctrls.controls, values)]


def set_control(fd, id, value):
    control = raw.v4l2_control(id, value)
    ioctl(fd, IOC.S_CTRL, control)


def _prepare_write_controls_values(control: raw.v4l2_query_ext_ctrl, value: object, raw_control: raw.v4l2_ext_control):
    raw_control.id = control.id
    has_payload = ControlFlag.HAS_PAYLOAD in ControlFlag(control.flags)
    if has_payload:
        if control.type == ControlType.STRING:
            raw_control.string = ctypes.create_string_buffer(value.encode())
            raw_control.size = len(value) + 1
        else:
            array_type = CTRL_TYPE_CTYPE_ARRAY.get(control.type)
            raw_control.size = control.elem_size * control.elems
            field = _field_for_control(control)
            # a struct: assume value is proper raw struct
            if array_type is None:
                value = ctypes.pointer(value)
            else:
                value = convert_to_ctypes_array(value, control.nr_of_dims, array_type)
            setattr(raw_control, field, value)
    else:
        if control.type == ControlType.INTEGER64:
            raw_control.value64 = value
        else:
            raw_control.value = value


def set_controls_values(
    fd, controls_values: list[tuple[raw.v4l2_query_ext_ctrl, object]], which=raw.ControlWhichValue.CUR_VAL, request_fd=0
):
    n = len(controls_values)
    ctrls = raw.v4l2_ext_controls()
    ctrls.which = which
    ctrls.count = n
    ctrls.request_fd = request_fd
    ctrls.controls = (n * raw.v4l2_ext_control)()
    for (control, value), raw_control in zip(controls_values, ctrls.controls):
        _prepare_write_controls_values(control, value, raw_control)
    ioctl(fd, IOC.S_EXT_CTRLS, ctrls)


def get_priority(fd) -> Priority:
    priority = ctypes.c_uint()
    ioctl(fd, IOC.G_PRIORITY, priority)
    return Priority(priority.value)


def set_priority(fd, priority: Priority):
    priority = ctypes.c_uint(priority.value)
    ioctl(fd, IOC.S_PRIORITY, priority)


def subscribe_event(
    fd,
    event_type: EventType = EventType.ALL,
    id: int = 0,
    flags: EventSubscriptionFlag = 0,
):
    sub = raw.v4l2_event_subscription()
    sub.type = event_type
    sub.id = id
    sub.flags = flags
    ioctl(fd, IOC.SUBSCRIBE_EVENT, sub)


def unsubscribe_event(fd, event_type: EventType = EventType.ALL, id: int = 0):
    sub = raw.v4l2_event_subscription()
    sub.type = event_type
    sub.id = id
    ioctl(fd, IOC.UNSUBSCRIBE_EVENT, sub)


def deque_event(fd):
    event = raw.v4l2_event()
    ioctl(fd, IOC.DQEVENT, event)
    return event


def set_edid(fd, edid):
    if len(edid) % 128:
        raise ValueError(f"EDID length {len(edid)} is not multiple of 128")
    edid_struct = raw.v4l2_edid()
    edid_struct.pad = 0
    edid_struct.start_block = 0
    edid_struct.blocks = len(edid) // 128
    edid_array = create_string_buffer(edid)
    edid_struct.edid = cast(edid_array, type(edid_struct.edid))
    ioctl(fd, IOC.S_EDID, edid_struct)


def clear_edid(fd):
    set_edid(fd, b"")


def get_edid(fd):
    edid_struct = raw.v4l2_edid()
    ioctl(fd, IOC.G_EDID, edid_struct)
    if edid_struct.blocks == 0:
        return b""
    edid_len = 128 * edid_struct.blocks
    edid_array = create_string_buffer(b"\0" * edid_len)
    edid_struct.edid = cast(edid_array, type(edid_struct.edid))
    ioctl(fd, IOC.G_EDID, edid_struct)
    return string_at(edid_struct.edid, edid_len)


def get_input(fd):
    inp = ctypes.c_uint()
    ioctl(fd, IOC.G_INPUT, inp)
    return inp.value


def set_input(fd, index: int):
    index = ctypes.c_uint(index)
    ioctl(fd, IOC.S_INPUT, index)


def get_output(fd):
    out = ctypes.c_uint()
    ioctl(fd, IOC.G_OUTPUT, out)
    return out.value


def set_output(fd, index: int):
    index = ctypes.c_uint(index)
    ioctl(fd, IOC.S_OUTPUT, index)


def get_std(fd):
    out = ctypes.c_uint64()
    ioctl(fd, IOC.G_STD, out)
    return out.value


def set_std(fd, std):
    ioctl(fd, IOC.S_STD, std)


def query_std(fd):
    out = ctypes.c_uint64()
    ioctl(fd, IOC.QUERYSTD, out)
    return out.value


# Helpers


def request_and_query_buffer(fd, buffer_type: BufferType, memory: Memory) -> raw.v4l2_buffer:
    """request + query buffers"""
    buffers = request_and_query_buffers(fd, buffer_type, memory, 1)
    return buffers[0]


def request_and_query_buffers(fd, buffer_type: BufferType, memory: Memory, count: int) -> list[raw.v4l2_buffer]:
    """request + query buffers"""
    request_buffers(fd, buffer_type, memory, count)
    return [query_buffer(fd, buffer_type, memory, index) for index in range(count)]


def mmap_from_buffer(fd, buff: raw.v4l2_buffer) -> mmap.mmap:
    return mem_map(fd, buff.length, offset=buff.m.offset)


def create_mmap_buffers(fd, buffer_type: BufferType, memory: Memory, count: int) -> list[mmap.mmap]:
    """create buffers + mmap_from_buffer"""
    return [mmap_from_buffer(fd, buff) for buff in request_and_query_buffers(fd, buffer_type, memory, count)]


def create_mmap_buffer(fd, buffer_type: BufferType, memory: Memory) -> mmap.mmap:
    return create_mmap_buffers(fd, buffer_type, memory, 1)


def enqueue_buffers(fd, buffer_type: BufferType, memory: Memory, count: int) -> list[raw.v4l2_buffer]:
    return [enqueue_buffer(fd, buffer_type, memory, 0, index) for index in range(count)]


def iter_video_files(path: PathLike = "/dev") -> Iterable[Path]:
    """Returns an iterator over all video files"""
    return iter_device_files(path=path, pattern="video*")


def iter_video_capture_files(path: PathLike = "/dev") -> Iterable[Path]:
    """Returns an iterator over all video files that have CAPTURE capability"""

    def filt(filename):
        with IO.open(filename) as fobj:
            caps = read_capabilities(fobj.fileno())
            return Capability.VIDEO_CAPTURE in Capability(caps.device_caps)

    return filter(filt, iter_video_files(path))


def iter_video_output_files(path: PathLike = "/dev") -> Iterable[Path]:
    """
    Some drivers (ex: v4l2loopback) don't report being output capable so that
    apps like zoom recognize them as valid capture devices so some results might
    be missing
    """

    def filt(filename):
        with IO.open(filename) as fobj:
            caps = read_capabilities(fobj.fileno())
            return Capability.VIDEO_OUTPUT in Capability(caps.device_caps)

    return filter(filt, iter_video_files(path))
