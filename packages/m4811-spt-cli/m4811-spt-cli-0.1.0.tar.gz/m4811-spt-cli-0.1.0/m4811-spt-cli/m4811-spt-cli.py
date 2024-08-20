#!/usr/bin/env python3

##############################################################################
#
# Module:  m4811-spt-cli.py
#
# Function:
#   Simple SPT emulator (from command line)
#
# Copyright and License:
#   Copyright (C) 2021, MCCI Corporation. See accompanying LICENSE file
#
# Author:
#   Terry Moore, MCCI   April, 2021
#
##############################################################################

import argparse
import collections
import csv
from datetime import datetime, timezone
import os
import re
import serial
import secrets
import struct
import sys
import time
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu, hooks
from enum import Enum
from pathlib import Path

global gVerbose
gVerbose = False

global gFile
gFile = b""

global gTestLogCsv
gTestLogCsv = Path("m4811-test-log.csv")
bin_file_path = "."

class kReg(Enum):
    Request = 0
    Status = 8
    FileSize = 16
    ProtocolVersion_u32 = 18

    DevEUI_u16x4 = 80
    AppEUI_u16x4 = 84
    AppKey_u16x8 = 88
    Region_u16 = 96
    CountryCode_u16 = 97
    NetworkCode_u16 = 98
    NetworkSubband_i16 = 99

    DevAddr_u32         = 112
    FCntUp_u32          = 114
    FCntDown_u32        = 116
    NetID_u32           = 118
    LinkIntegrity_i16   = 120
    LinkDR_u16          = 121
    TxPower_u16         = 122
    DownlinkRSSI_i16    = 123

    WattNodeSerial_u32  = 128
    WattNodeUptime_u32  = 130
    WattNodeRuntime_u32 = 132
    WattNodeModel_u16   = 134
    WattNodeVersion_u16 = 135

    WN_CtAmps1_u16      = 160
    WN_CtAmps2_u16      = 161
    WN_CtAmps3_u16      = 162
    WN_CtDirections_u16 = 163
    WN_MeterConfig1_u16 = 164
    WN_MeterConfig2_u16 = 165
    WN_MeterConfig3_u16 = 166

    PowerSum_f32        = 192
    Power1_f32          = 194
    Power2_f32          = 196
    Power3_f32          = 198
    VoltAvgLN_f32       = 200
    VoltAvgAN_f32       = 202
    VoltAvgBN_f32       = 204
    VoltAvgCN_f32       = 206
    VoltAvgLL_f32       = 208
    VoltAvgAB_f32       = 210
    VoltAvgBC_f32       = 212
    VoltAvgCA_f32       = 214
    Freq_f32            = 216
    Current1_f32        = 218
    Current2_f32        = 220
    Current3_f32        = 222

    FirmwareVersion_u32         = 0x100
    FirmwareImageSize_u32       = 0x102
    FirmwareTime_u64            = 0x104
    FirmwarePublic_u16x16       = 0x108
    FirmwareHash_u16x32         = 0x118
    FirmwareSignature_u16x32    = 0x138

    BootloaderVersion_u32       = 0x200
    BootloaderImageSize_u32     = 0x202
    BootloaderTime_u64          = 0x204
    BootloaderPublic_u16x16     = 0x208
    BootloaderHash_u16x32       = 0x218
    BootloaderSignature_u16x32  = 0x238
    BootloaderSignature_end     = 0x258

    FileData = 0x8000

class kRq(Enum):
    kNone = 0
    kGetFirmwareVersion = 0x0001
    kLoadFirmware = 0x0102
    kReportNetworkParameters = 0x0003
    kSetAppEUI = 0x0104
    kSetAppKey = 0x0105
    kRejoin = 0x0106
    kCheckConnection = 0x0107
    kGetWattNodeSerial = 0x0008
    kGetWattNodeConfig = 0x0009
    kGetWattNodeStatus = 0x000A
    kReservedB = 0x000B
    kSetCtAmps = 0x010C
    kSetCtDirections = 0x010D
    kSetMeterConfig = 0x010E
    kReboot = 0x010F
    kGetBootloaderVersion= 0x0010
    kGetNetworkStatus = 0x0011
    kSetDevEUI = 0x0112
    kGetProtocolVersion = 0x0013

class kStatus(Enum):
    Pending                 = 0
    Successful              = 1
    InvalidRequest          = 2
    DownloadSizeTooBig      = 3
    DownloadSizeReadError   = 4
    DownloadReadError       = 5
    DownloadSizeTooSmall    = 6
    HashCheckFailure        = 7
    UpdateFlagLocateFailure = 8
    UpdateFlagSetFailure    = 9
    kNotImplemented         = 10
    SptWriteError           = 11
    WattNodeReadError       = 12
    FramFailure             = 13
    UplinkNotProvisioned    = 14
    UplinkFailed            = 15
    UplinkRejected          = 16
    UplinkOverrun           = 17
    UplinkOtherError        = 18
    CtAmpsReadError         = 19
    CtAmpsWriteError        = 20
    CtDirectionsReadError   = 21
    CtDirectionsWriteError  = 22
    MeterConfigReadError    = 23
    MeterConfigWriteError   = 24

global kNetworkID
kNetworkID = {
    0: "The Things Network",
    1: "Actility",
    2: "Helium",
    3: "machineQ",
    4: "Senet",
    5: "Senra",
    6: "Swisscom",
    7: "ChirpStack",
    8: "Generic",
    }

global kRegionID
kRegionID = {
    1: "EU868",
    2: "US915",
    3: "CN783",
    4: "EU433",
    5: "AU915",
    6: "CN490",
    7: "AS923",
    8: "KR920",
    9: "IN866",
}

global gAddress
gAddress = 0

##############################################################################
#
# Name: ParseCommandArgs()
#
# Function:
#   Parse the command line arguments
#
# Definition:
#   ParseCommandArgs() -> Namespace
#
##############################################################################

def ParseCommandArgs():
    def checkPath(s):
        result = Path(s)
        if not result.is_dir():
            raise ValueError(f"'{s}' is not a directory")
        return result

    # Example usage
    try:
        dir_path = checkPath(bin_file_path)
    except ValueError as e:
        print("Error:", e)

    parser = argparse.ArgumentParser(description="Site-provisioning tool emulator")
    parser.add_argument(
        "sComPort", metavar="{portname}",
        help="COM port to be used to communicate with 4811"
        )
    parser.add_argument(
        "--baud", "-b",
        help="baud rate",
        default=19200
        )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="verbose output",
        default=False
        )
    parser.add_argument(
        "tCommand", metavar="{command}",
        nargs="*",
        help="command to send to the Model 4811"
        )
    return parser.parse_args()

# wait for completion
def send_cmd_await_status(spt, rq, cmdname):
    spt.set_values("Status", kReg.Status.value, [ 0, 0, 0] )
    spt.set_values("Request", kReg.Request.value, [ rq.value, 1 ])

    while True:
        v = spt.get_values("Status", kReg.Status.value, 3)
        if v[2] != kStatus.Pending.value:
            if v[2] == kStatus.Successful.value:
                print(f"{cmdname} request succeeded!")
                return True
            else:
                print(f"{cmdname} failed, status kStatus.{kStatus(v[2]).name}({v[2]})")
                return False

# do the download
def do_download(spt, filename):
    global gFile
    global gAddress
    try:
        f = open(filename, mode="rb")
        gFile = f.read()
        f.close()
    except:
        print("can't open:", filename, sys.exc_info())
        return kStatus.InvalidRequest

    filesize = len(gFile)

    spt.set_values("FileSize", kReg.FileSize.value, [ filesize >> 16, filesize & 0xFFFF ])
    (fshi, fslo) = spt.get_values("FileSize", kReg.FileSize.value, 2)

    spt.set_values("Status", kReg.Status.value, [ 0, 0, 0] )

    lastAddress = gAddress

    print(f"Triggering download of 0x{filesize:x} bytes")
    spt.set_values("Request", kReg.Request.value, [ kRq.kLoadFirmware.value, 1 ])
    while True:
        v = spt.get_values("Status", kReg.Status.value, 3)
        if v[2] != 0:
            if v[2] == 1:
                print("Download succeeded!")
                return kStatus.Successful
            else:
                print(f"Download failed, status kStatus.{kStatus(v[2]).name}({v[2]})")
                return kStatus(v[2])
        if lastAddress != gAddress:
            print(".", sep='', end='', flush=True)
            gAddress = lastAddress

def do_reboot(spt):
    return send_cmd_await_status(spt, kRq.kReboot, "reboot")

def fmtVersion(v):
    major = (v >> 24) & 0xFF
    minor = (v >> 16) & 0xFF
    patch = (v >> 8) & 0xFF
    pre = (v >> 0) & 0xFF
    result = f"{major}.{minor}"
    if patch != 0:
        result += f".{patch}"
    if pre != 0:
        result += f"-pre{pre}"
    return result

def getUint32(spt, rv, block="General"):
    (hi, lo) = spt.get_values(block, rv, 2)
    return ((hi & 0xFFFF) << 16) | (lo & 0xFFFF)

def getUint64(spt, rv):
    (hi, mh, ml, lo) = spt.get_values("General", rv, 4)
    return ((hi & 0xFFFF) << 48) | ((mh & 0xFFFF) << 32) | ((ml & 0xFFFF) << 16) | (lo & 0xFFFF)

def getUint16(spt,rv):
    (result,) = spt.get_values("General", rv, 1)
    return result & 0xFFFF

def getInt16(spt,rv):
    (result,) = spt.get_values("General", rv, 1)
    if result >= 32768:
        result = result - 65536
    return result

def getBytes(spt, rv, nb):
    result = b''
    while nb > 1:
        (r,) = spt.get_values("General", rv, 1)
        rv = rv + 1
        nb = nb - 2
        result += bytes([ (r >> 8) & 0xFF, r & 0xFF])
    if nb > 0:
        (r,) = spt.get_values("General", rv, 1)
        result += bytes([ (r >> 8) & 0xFF ])
    return result

def getFloat32(spt, rv):
    return struct.unpack('>f', getBytes(spt, rv, 4))[0]

def fmtBytes(b, indent):
    i = 0
    istr = "\n" + (" " * indent)
    result = ""
    while b[i:i+16] != b"":
        if i > 0:
            result += istr
        result += b[i:i+16].hex('-')
        i += 16
    return result

def do_getversion_protocol(spt):
    if send_cmd_await_status(spt, kRq.kGetProtocolVersion, f"get version protocol"):
        # display protocol version info
        print(f"Protocol:   {fmtVersion(getUint32(spt, kReg.ProtocolVersion_u32.value, 'ProtocolVersion'))}")

def do_getversion(spt, tArgs):
    rq = kRq.kNone.value
    offset = 0
    if tArgs[0] == "app":
        rq = kRq.kGetFirmwareVersion
        offset = 0
    elif tArgs[0] == "bootloader":
        rq = kRq.kGetBootloaderVersion
        offset = kReg.BootloaderVersion_u32.value - \
                 kReg.FirmwareVersion_u32.value
    elif tArgs[0] == "protocol":
        do_getversion_protocol(spt)
        return
    else:
        print(f"Unknown version parameter: {tArgs[0]}")
        return

    if send_cmd_await_status(spt, rq, f"get {tArgs[0]} version"):
        # display the version info
        print(f"Version:     {fmtVersion(getUint32(spt, kReg.FirmwareVersion_u32.value + offset))}")
        print(f"Size:        {getUint32(spt, kReg.FirmwareImageSize_u32.value + offset)}")
        t = getUint64(spt, kReg.FirmwareTime_u64.value + offset)
        print(f"Time:        {datetime.fromtimestamp(t, timezone.utc)}")
        pk = getBytes(spt, kReg.FirmwarePublic_u16x16.value + offset, 32)
        print(f"Public Key:  {fmtBytes(pk, 13)}")
        sha = getBytes(spt, kReg.FirmwareHash_u16x32.value + offset, 64)
        print(f"Hash:        {fmtBytes(sha, 13)}")
        sig = getBytes(spt, kReg.FirmwareSignature_u16x32.value + offset, 64)
        print(f"Signature:   {fmtBytes(sig, 13)}")

def fmtUint64(spt, rv):
    v = getUint64(spt, rv)
    return struct.pack(">Q", v).hex('-')

def fmtCountryCode(code):
    if code == 0:
        return "none"
    c1 = bytes([code >> 8])
    c2 = bytes([code & 0xFF])
    if c1 < b'A' or c1 > b'Z' or c2 < b'A' or c2 > b'Z':
        return "unknown(0x%x)" % code
    else:
        return (c1 + c2).decode()

def fmtRegion(region):
    if region in kRegionID:
        return kRegionID[region]
    return f"unknown-region({region})"

def fmtSubband(code, region):
    regionName = fmtRegion(region)
    channels = 16
    if regionName == "US915" or regionName == "AU915":
        channels = 64
    elif  regionName == "CN783":
        channels = 96
    elif code != -1:
        return "unknown value for region(%x)" % code
    else:
        return "no subbands"

    if code == -1:
        return f"0~{channels-1}/{channels}~{channels + (channels >> 3) - 1}"
    else:
        return f"{code*8}~{code*8+7}/{channels+code}"

def do_getnetworkprovisioning(spt):
    if send_cmd_await_status(spt, kRq.kReportNetworkParameters, "ReportNetworkParameters"):
        # display results
        print(f"DevEUI:       {fmtUint64(spt, kReg.DevEUI_u16x4.value)}")
        print(f"AppEUI:       {fmtUint64(spt, kReg.AppEUI_u16x4.value)}")
        appKey = getBytes(spt, kReg.AppKey_u16x8.value, 16)
        appKey_string = fmtBytes(appKey, 14)
        if appKey == b'\0' * 16:
            appKey_string = '**-' * 15 + '**'
        print(f"AppKey:       {appKey_string}")
        regionCode = getUint16(spt, kReg.Region_u16.value)
        regionName = "<<unknown>>"
        if regionCode in kRegionID:
            regionName = kRegionID[regionCode]
        print(f"Region:       {regionName} ({regionCode})")
        print(f"Country Code: {fmtCountryCode(getUint16(spt, kReg.CountryCode_u16.value))}")

        networkCode = getUint16(spt, kReg.NetworkCode_u16.value)
        networkName = "<<unknown>>"
        if networkCode in kNetworkID:
            networkName = kNetworkID[networkCode]

        print(f"Network:      {networkName} ({networkCode})")
        print(f"Subband:      {fmtSubband(getInt16(spt, kReg.NetworkSubband_i16.value), regionCode)}")

def do_getnetworkstatus(spt):
    if send_cmd_await_status(spt, kRq.kGetNetworkStatus, "GetNetworkStatus"):
        # display resutls
        print(f"DevAddr:       0x{getUint32(spt, kReg.DevAddr_u32.value):08x}")
        print(f"FCntUp:        {getUint32(spt, kReg.FCntUp_u32.value)}")
        print(f"FCntDown:      {getUint32(spt, kReg.FCntDown_u32.value)}")
        print(f"NetID:         0x{getUint32(spt, kReg.NetID_u32.value):08x}")
        print(f"LinkIntegrity: {getInt16(spt, kReg.LinkIntegrity_i16.value)}")
        print(f"LinkDr:        {getUint16(spt, kReg.LinkDR_u16.value)}")
        print(f"TxPower:       {getUint16(spt, kReg.TxPower_u16.value)}")
        print(f"DownlinkRSSI:  {getInt16(spt, kReg.DownlinkRSSI_i16.value)}")

def do_getnetwork(spt, tArgs):
    if tArgs[0] == "provisioning":
        return do_getnetworkprovisioning(spt)
    elif tArgs[0] == "status":
        return do_getnetworkstatus(spt)
    else:
        print(f"get network: invalid: {tArgs[0]}")
        return False

def do_getmeter_info(spt):
    if send_cmd_await_status(spt, kRq.kGetWattNodeSerial, "GetWattNodeSerial"):
        # display results
        print(f"Serial:       {getUint32(spt, kReg.WattNodeSerial_u32.value)}")
        print(f"Uptime:       {getUint32(spt, kReg.WattNodeUptime_u32.value)}")
        print(f"Total time:   {getUint32(spt, kReg.WattNodeRuntime_u32.value)}")
        print(f"Model:        {getUint16(spt, kReg.WattNodeModel_u16.value)}")
        print(f"Version:      {getUint16(spt, kReg.WattNodeVersion_u16.value)}")

def do_getmeter_config(spt):
    if send_cmd_await_status(spt, kRq.kGetWattNodeConfig, "GetWattNodeConfig"):
        # display results
        print(f"CtAmps1:      {getUint16(spt, kReg.WN_CtAmps1_u16.value)}")
        print(f"CtAmps2:      {getUint16(spt, kReg.WN_CtAmps2_u16.value)}")
        print(f"CtAmps3:      {getUint16(spt, kReg.WN_CtAmps3_u16.value)}")
        print(f"CtDirections: {getUint16(spt, kReg.WN_CtDirections_u16.value)}")
        print(f"MeterConfig1: {getUint16(spt, kReg.WN_MeterConfig1_u16.value)}")
        print(f"MeterConfig2: {getUint16(spt, kReg.WN_MeterConfig2_u16.value)}")
        print(f"MeterConfig3: {getUint16(spt, kReg.WN_MeterConfig3_u16.value)}")

def do_getmeter_status(spt):
    if send_cmd_await_status(spt, kRq.kGetWattNodeStatus, "GetWattNodeStatus"):
        # display results
        print(f"PowerSum:     {getFloat32(spt, kReg.PowerSum_f32.value)}")
        print(f"Power1:       {getFloat32(spt, kReg.Power1_f32.value)}")
        print(f"Power2:       {getFloat32(spt, kReg.Power2_f32.value)}")
        print(f"Power3:       {getFloat32(spt, kReg.Power3_f32.value)}")
        print(f"VoltAvgLN     {getFloat32(spt, kReg.VoltAvgLN_f32.value)}")
        print(f"VoltAvgAN     {getFloat32(spt, kReg.VoltAvgAN_f32.value)}")
        print(f"VoltAvgBN     {getFloat32(spt, kReg.VoltAvgBN_f32.value)}")
        print(f"VoltAvgCN     {getFloat32(spt, kReg.VoltAvgCN_f32.value)}")
        print(f"VoltAvgLL     {getFloat32(spt, kReg.VoltAvgLL_f32.value)}")
        print(f"VoltAvgAB     {getFloat32(spt, kReg.VoltAvgAB_f32.value)}")
        print(f"VoltAvgBC     {getFloat32(spt, kReg.VoltAvgBC_f32.value)}")
        print(f"VoltAvgCA     {getFloat32(spt, kReg.VoltAvgCA_f32.value)}")
        print(f"Freq          {getFloat32(spt, kReg.Freq_f32.value)}")
        print(f"Current1      {getFloat32(spt, kReg.Current1_f32.value)}")
        print(f"Current2      {getFloat32(spt, kReg.Current2_f32.value)}")
        print(f"Current3      {getFloat32(spt, kReg.Current3_f32.value)}")

def do_getmeter(spt, tArgs):
    if tArgs[0] == "info":
        return do_getmeter_info(spt)
    elif tArgs[0] == "config":
        return do_getmeter_config(spt)
    elif tArgs[0] == "status":
        return do_getmeter_status(spt)
    else:
        print(f"get meter: invalid: {tArgs[0]}")

def scanBytes(s, nbytes):
    result = b''
    s = s.replace("-", " ")
    m = re.findall(r"([0-9a-fA-f]{1,2})", s)
    for i in m:
        result += bytes.fromhex(i.zfill(2))
    return (result + b'\0' * nbytes)[0:nbytes]

def do_setappeui(spt, tArgs):
    b = scanBytes(tArgs[0], 8)
    spt.set_values("General", kReg.AppEUI_u16x4.value, struct.unpack('>4H', b))
    return send_cmd_await_status(spt, kRq.kSetAppEUI, "SetAppEUI")

def do_setdeveui(spt, tArgs):
    b = scanBytes(tArgs[0], 8)
    spt.set_values("General", kReg.DevEUI_u16x4.value, struct.unpack('>4H', b))
    return send_cmd_await_status(spt, kRq.kSetDevEUI, "SetDevEUI")

def do_setappkey(spt, tArgs):
    b = scanBytes(tArgs[0], 16)
    spt.set_values("General", kReg.AppKey_u16x8.value, struct.unpack('>8H', b))
    return send_cmd_await_status(spt, kRq.kSetAppKey, "SetAppKey")

def do_setctamps(spt, tArgs):
    ct1 = int(tArgs[0])
    ct2 = int(tArgs[1])
    ct3 = int(tArgs[2])
    spt.set_values("General", kReg.WN_CtAmps1_u16.value, [ ct1, ct2, ct3 ])
    send_cmd_await_status(spt, kRq.kSetCtAmps, "set CT amps")

def do_setctdir(spt, tArgs):
    dirs = int(tArgs[0])
    spt.set_values("General", kReg.WN_CtDirections_u16.value, [ dirs ])
    send_cmd_await_status(spt, kRq.kSetCtDirections, "set CT directions")

def do_setmetercfg(spt, tArgs):
    meter1 = int(tArgs[0])
    meter2 = int(tArgs[1])
    meter3 = int(tArgs[2])
    spt.set_values("General", kReg.WN_MeterConfig1_u16.value, [ meter1, meter2, meter3 ])
    send_cmd_await_status(spt, kRq.kSetMeterConfig, "set meter config")

def do_rejoin(spt):
    return send_cmd_await_status(spt, kRq.kRejoin, "rejoin")

def do_checkconnection(spt):
    send_cmd_await_status(spt, kRq.kCheckConnection, "check connection")

def do_mfg_inner(spt, file):
    # do the manufacturing test:
    # 1. download firmware; retry if failures.
    result = collections.namedtuple(
        'MfgResult',
        "serial error devEUI appEUI appKey appVersion",
        defaults = [ None, None, "-", "-", "-", "-"  ]
        )

    if file != "-":
        while True:
            rc = do_download(spt, file)
            if rc == kStatus.Successful:
                break
            if rc != kStatus.DownloadReadError:
                result.error = "Unrecoverable mfg download error"
                return result
            pass

        # 2. reboot
        if not do_reboot(spt):
            result.error = "reboot failed"
            return result

        # 3. wait for boot to finish
        time.sleep(5)

    # 4. get the serial number of the device
    if not send_cmd_await_status(spt, kRq.kGetWattNodeSerial, "GetWattNodeSerial"):
        result.error = "can't get serial number"
        return result

    # 5. covert to a dev eui
    serial = getUint32(spt, kReg.WattNodeSerial_u32.value)
    result.serial  = serial
    devEUI_string = "0002CC02%08d" % serial
    result.devEUI = devEUI_string

    # 6. download the dev eui to the device
    print("mfg: set deveui to %s" % devEUI_string)
    if not do_setdeveui(spt, [ devEUI_string ]):
        result.error = "can't set deveui"
        return result

    # 7. zero the app eui
    appEUI_string = "0000000000000001"
    result.appEUI = appEUI_string
    print("mfg: set appeui to %s" % appEUI_string)
    if not do_setappeui(spt, [ appEUI_string ]):
        result.error = "can't set appeui"
        return result

    # 8. get the appkey
    appKey = b""
    if not send_cmd_await_status(spt, kRq.kReportNetworkParameters, "ReportNetworkParameters"):
        result.error = "couldn't fetch network params"
        return result

    appKey = getBytes(spt, kReg.AppKey_u16x8.value, 16)
    if appKey == b'\0' * 16:
        # zero app key says we can't use what came from device
        # generate a key
        appKey = secrets.token_bytes(16)
        if not do_setappkey(spt, [ fmtBytes(appKey, 0) ]):
            result.error = "couldn't set appkey"
            return result

    # display results
    print(f"DevEUI:       {fmtUint64(spt, kReg.DevEUI_u16x4.value)}")
    print(f"AppEUI:       {fmtUint64(spt, kReg.AppEUI_u16x4.value)}")
    print(f"AppKey:       {fmtBytes(appKey, 14)}")
    result.appKey = fmtBytes(appKey, 0)

    # 9. force a join
    if not do_rejoin(spt):
        result.error = "rejoin failed"
        return result

    # 9. get the software version
    if send_cmd_await_status(spt, kRq.kGetFirmwareVersion, f"getFirmwareVersion"):
        # display the version info
        appVersion = fmtVersion(getUint32(spt, kReg.FirmwareVersion_u32.value))
        result.appVersion = appVersion
        print(f"Version:     {appVersion}")
    else:
        result.error = "couldn't read app version"
        return result

    # 10. write to the csv file: s/n, devEUI, appEUI, Appkey, software version -- caller does it.
    result.error = None
    return result

def read_resultCsv(spt, sFile):
    t = {}
    try:
        with open(sFile, newline='') as f:
            r = csv.reader(f)
            for row in r:
                t[row[0]] = row
    except:
        print("can't open test reult file, try touching to make an empty file:", sFile, sys.exc_info())
        sys.exit(1)

    return t

def do_mfg(spt, tArgs):
 # Ensure the directory for the log file exists
    log_dir = gTestLogCsv.parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {log_dir}")

    # Try opening the file, create it if it doesn't exist
    try:
        with open(gTestLogCsv, 'a') as f:
            gFile = f
            # print("gfile--->:", gFile)
            # f.write("\n")
    except FileNotFoundError:
        print(f"Can't open or create log file: {gTestLogCsv}")

    filename = tArgs[0] if len(tArgs) > 0 else "-"
    result = do_mfg_inner(spt, filename)
    
    if result.error is not None:
        print("mfg failed: %s" % result.error)
        while result.serial is None:
            serial_str = input("serial? ")
            try:
                result.serial = int(serial_str)
            except:
                pass
        result.disposition = input("disposition? ")
    else:
        result.error = ""
        result.disposition = ""

    # Create entry
    now = datetime.now().replace(microsecond=0).isoformat()
    sPassed = "OK" if result.error == "" else "FAILED"
    tThis = [
        f"{result.serial}",
        now,
        result.devEUI,
        result.appEUI,
        result.appKey,
        result.appVersion,
        sPassed,
        result.error,
        result.disposition
    ]

    # Open the CSV file in append mode and write the new result
    with open(gTestLogCsv, "a", newline='') as outfile:
        w = csv.writer(outfile)
        w.writerow(tThis)

    if result.error == "":
        print("passed!")
        print(f"Data stored in'{gTestLogCsv}' successfully.")
        return True
    else:
        print("failed!")
        print(f"Data storing in'{gTestLogCsv}' failed.")
        return False


# this is called on every read of holding registers
# it must filter file read operations and quickly update the
# referenced holding registers with the appropriate slice
# of the file. This can also be used to detect the periodic polling
# that the SPT does
def onReadHolding(args):
    global gAddress
    (hDevice, pdu) = args
    starting_address = struct.unpack(">H", pdu[1:3])[0]
    if (starting_address < kReg.FileData.value or starting_address > kReg.FileData.value + len(gFile) / 250):
        return
    file_offset = (starting_address - kReg.FileData.value) * 250
    filebuf = gFile[file_offset : file_offset + 250]

    # this is not very efficient, as we unpack here and repack inside set_values().
    # However, this sets the registers that will subsequently be returned to be
    # the appropriate slice of the file.
    hDevice.set_values(
        "File",
        starting_address,
        # big-endian, as many entries as needed
        struct.unpack(">" + ("H" * int(len(filebuf)/2)), filebuf[0:250])
        )
    gAddress = starting_address

# This is called on every write of holding registers.
# It detects writes to the status and clears the command.
def onWriteMultiple(args):
    (hDevice, pdu) = args
    starting_address = struct.unpack(">H", pdu[1:3])[0]
    if (starting_address == kReg.Status.value):
        hDevice.set_values("Request", kReg.Request.value, [ 0, 0])
    elif gVerbose:
        print(f"PDU: {fmtBytes(pdu,5)}")

# main function
def main():
    global gVerbose
    global gFile
    global gTestLogCsv
    
    args = ParseCommandArgs()
    gVerbose = args.verbose

    # open the serial port
    hPort = serial.Serial(args.sComPort, baudrate=args.baud)
    if gVerbose:
        print("Using port {}".format(hPort.name))

    # create the server
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(name)-12s: %(levelname)-8s %(message)s")
    server = modbus_rtu.RtuServer(hPort)
    hooks.install_hook("modbus.Slave.handle_read_holding_registers_request", onReadHolding)
    hooks.install_hook("modbus.Slave.handle_write_multiple_registers_request", onWriteMultiple)

    try:
        logger.info("m4811-spt-cli running...")
        logger.info("enter 'quit' to exit")

        server.start()
        spt = server.add_slave(247)
        spt.add_block("Request", cst.HOLDING_REGISTERS, kReg.Request.value, 2)
        spt.add_block("Status", cst.HOLDING_REGISTERS, kReg.Status.value, 3)
        spt.add_block("FileSize", cst.HOLDING_REGISTERS, kReg.FileSize.value, 2)
        spt.add_block("ProtocolVersion", cst.HOLDING_REGISTERS, kReg.ProtocolVersion_u32.value, 2)

        spt.add_block("General", cst.HOLDING_REGISTERS, kReg.DevEUI_u16x4.value, kReg.BootloaderSignature_end.value - kReg.DevEUI_u16x4.value)

        # the file image, but overridden by the hooks
        spt.add_block("File", cst.HOLDING_REGISTERS, kReg.FileData.value, int(((192 * 1024 / 2) + 124) / 125) + 125)
        spt.set_values("Request", kReg.Request.value, [0, 0])
        while True:
            cmd = sys.stdin.readline()
            args = cmd.rstrip().split(' ')
            if cmd.find('quit') == 0:
                sys.stdout.write("exiting\r\n")
                break
            elif args[0] == "download":
                # do a download
                do_download(spt, args[1])
            elif args[0] == "mfg":
                # do mfg test
                do_mfg(spt, args[1:])
            elif args[0] == "reboot":
                # reboot the 4811
                do_reboot(spt)
            elif args[0] == "get" and args[1] == "version":
                do_getversion(spt, args[2:])
            elif args[0] == "get" and args[1] == "network":
                do_getnetwork(spt, args[2:])
            elif args[0] == "get" and args[1] == "meter":
                do_getmeter(spt, args[2:])
            elif args[0] == "set" and args[1] == "appeui":
                do_setappeui(spt, args[2:])
            elif args[0] == "set" and args[1] == "deveui":
                do_setdeveui(spt, args[2:])
            elif args[0] == "set" and args[1] == "appkey":
                do_setappkey(spt, args[2:])
            elif args[0] == "set" and args[1] == "ctamps":
                do_setctamps(spt, args[2:] )
            elif args[0] == "set" and args[1] == "ctdir":
                do_setctdir(spt, args[2:])
            elif args[0] == "set" and args[1] == "meter":
                do_setmetercfg(spt, args[2:])
            elif args[0] == "rejoin":
                do_rejoin(spt)
            elif args[0] == "check" and args[1] == "connection":
                do_checkconnection(spt)
            else:
                print("unknown request:", cmd)

    finally:
        server.stop()

#### the standard trailer #####
if __name__ == '__main__':
    main()
