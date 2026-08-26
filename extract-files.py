#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/vicky',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'vendor/mediatek/ims',
    'hardware/motorola',
    'hardware/google/pixel',
    'hardware/google/interfaces',
    'hardware/millenium',
    'hardware/millenium/libtranlog',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

patchelf_version = "0_17_2"

blob_fixups: blob_fixups_user_type = {
    ('vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc'): blob_fixup()
        .regex_replace('start', 'enable'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v31.so')
        .replace_needed('libcodec2_hidl@1.2.so', 'libcodec2_hidl@1.2-v31.so'),
    'vendor/etc/init/android.hardware.media.c2@1.2-mediatek-64b.rc': blob_fixup()
        .add_line_if_missing('    interface android.hardware.media.c2@1.0::IComponentStore default')
        .add_line_if_missing('    interface android.hardware.media.c2@1.1::IComponentStore default')
        .add_line_if_missing('    interface android.hardware.media.c2@1.2::IComponentStore default')
        .regex_replace('mediatek', 'mediatek-64b'),
    'vendor/etc/vintf/manifest/manifest_media_c2_V1_2_default.xml': blob_fixup()
        .regex_replace('1.1', '1.2')
        .regex_replace('@1.0', '@1.2'),
    'vendor/lib64/libcodec2_hidl@1.0-v31.so': blob_fixup()
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v31.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),
    'vendor/lib64/libcodec2_hidl@1.1-v31.so': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v31.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),
    # Fix host_init_verifier error by stripping dead ATCI interface
    'vendor/etc/init/atcid.rc': blob_fixup()
        .regex_replace(r'interface vendor\.mediatek\.hardware\.atci@1\.0::IAtcid default', ''),
        
    # Fix host_init_verifier error by stripping dead DMC/APMonitor interfaces
    'vendor/etc/init/dmc_core.rc': blob_fixup()
        .regex_replace(r'interface vendor\.mediatek\.hardware\.apmonitor@2\.0::IApmService default', '')
        .regex_replace(r'interface vendor\.mediatek\.hardware\.dmc@[0-9\.]+::IDmcService default', ''),
    'vendor/lib64/libcodec2_hidl@1.2-v31.so': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v31.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v31.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/libcodec2_mtk_c2store.so', 'vendor/lib64/libcodec2_vpp_qt_plugin.so', 'vendor/lib64/libcodec2_vpp_rs_plugin.so'): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    ('vendor/lib64/libcodec2_mtk_vdec.so', 'vendor/lib64/libcodec2_mtk_venc.so'): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    'vendor/lib64/libcodec2_vndk-v31.so': blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/lib64/libsfplugin_ccodec_utils-v31.so': blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/bin/hw/vendor.mediatek.hardware.mtkpower@1.0-service': blob_fixup()
    .replace_needed('android.hardware.power-V2-ndk_platform.so', 'android.hardware.power-V2-ndk.so'),
    ('vendor/bin/mnld', 'vendor/lib64/hw/android.hardware.sensors@2.X-subhal-mediatek.so', 'vendor/lib64/mt6789/libcam.utils.sensorprovider.so'): blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/hw/mt6789/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libutils.so','libutils-v32.so')
        .replace_needed('libalsautils.so','libalsautils-v31.so'),
    ('vendor/lib64/mt6789/libcam.hal3a.v3.so', 'vendor/lib64/hw/hwcomposer.mtk_common.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    ('vendor/lib/mt6789/libneuralnetworks_sl_driver_mtk_prebuilt.so', 'vendor/lib64/mt6789/libneuralnetworks_sl_driver_mtk_prebuilt.so', 
     'vendor/lib64/libstfactory-vendor.so', 'vendor/lib/libnvram.so', 'vendor/lib64/libnvram.so',
     'vendor/lib/libsysenv.so', 'vendor/lib64/libsysenv.so', 'vendor/lib/libtflite_mtk.so', 'vendor/lib64/libtflite_mtk.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/hw/mt6789/android.hardware.camera.provider@2.6-impl-mediatek.so','vendor/lib64/mt6789/libmtkcam_stdutils.so',
     'vendor/lib64/sensors.moto.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/mt6789/lib3a.flash.so', 'vendor/lib64/mt6789/lib3a.ae.stat.so',
     'vendor/lib64/mt6789/lib3a.sensors.flicker.so', 'vendor/lib64/mt6789/lib3a.sensors.color.so',
     'vendor/lib64/mt6789/libaaa_ltm.so', 'vendor/lib64/lib3a.ae.pipe.so'): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/mt6789/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek', 'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
        .replace_needed(
            'android.hardware.security.keymint-V1-ndk_platform.so',
            'android.hardware.security.keymint-V1-ndk.so',
        )
        .replace_needed(
            'android.hardware.security.secureclock-V1-ndk_platform.so',
            'android.hardware.security.secureclock-V1-ndk.so',
        )
        .replace_needed(
            'android.hardware.security.sharedsecret-V1-ndk_platform.so',
            'android.hardware.security.sharedsecret-V1-ndk.so',
        )
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    # Fix for trustonic keymint service
    'vendor/bin/hw/android.hardware.security.keymint-service.trustonic': blob_fixup()
        .replace_needed(
            'android.hardware.security.keymint-V1-ndk_platform.so',
            'android.hardware.security.keymint-V1-ndk.so',
        )
        .replace_needed(
            'android.hardware.security.secureclock-V1-ndk_platform.so',
            'android.hardware.security.secureclock-V1-ndk.so',
        )
        .replace_needed(
            'android.hardware.security.sharedsecret-V1-ndk_platform.so',
            'android.hardware.security.sharedsecret-V1-ndk.so',
        ),
    # Fix for libminiui dependency - replace with libminui
    ('vendor/bin/factory', 'vendor/lib64/libcameracustom.so'): blob_fixup()
        .replace_needed('libminiui.so', 'libminui.so'),
    'vendor/bin/qcc-trd': blob_fixup()
        .replace_needed(
            'libgrpc++_unsecure.so', 'libgrpc++_unsecure_prebuilt.so'
        ),
    'vendor/etc/media_codecs_c2_audio.xml': blob_fixup()
        .regex_replace('.+media_codecs_dolby_audio.+\n', ''),
    # Fix remaining ndk_platform dependencies
    # 'vendor/lib64/motorola.hardware.sarwifi-V1-ndk_platform.so': blob_fixup()
    #     .replace_needed('motorola.hardware.sarwifi-V1-ndk_platform.so', 'motorola.hardware.sarwifi-V1-ndk.so'),
    # Fix shared_libs dependencies that reference ndk_platform libraries
    ('vendor/lib/egl/mt6789/libGLES_mali.so', 'vendor/lib64/egl/mt6789/libGLES_mali.so'): blob_fixup()
        .replace_needed('arm.graphics-V1-ndk.so', 'arm.graphics-V1-ndk_platform.so'),
    ('vendor/lib/hw/mt6789/android.hardware.graphics.mapper@4.0-impl-mediatek.so', 'vendor/lib64/hw/mt6789/android.hardware.graphics.mapper@4.0-impl-mediatek.so'): blob_fixup()
        .replace_needed('arm.graphics-V1-ndk.so', 'arm.graphics-V1-ndk_platform.so'),
    # Fix remaining ndk_platform dependencies in factory binary
    'vendor/bin/factory': blob_fixup()
        .replace_needed('android.hardware.light-V1-ndk_platform.so', 'android.hardware.light-V1-ndk.so'),
    # 'vendor/bin/hw/motorola.hardware.sarwifi-srv': blob_fixup()
    #     .replace_needed('motorola.hardware.sarwifi-V1-ndk.so', 'motorola.hardware.sarwifi-V1-ndk_platform.so'),
    # Fix missing dependency modules
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .replace_needed('libalsautils-v31.so', 'libalsautilsv2.so'),
    'vendor/bin/hw/android.hardware.gnss-service.mediatek': blob_fixup()
        .replace_needed('android.hardware.gnss-impl-mediatek.so', 'android.hardware.gnss-impl-mediatek.so'),
    # Fix libacdk dependency to use libminui instead of libminiui
    'vendor/lib64/mt6789/libacdk.so': blob_fixup()
        .replace_needed('libminiui.so', 'libminui.so'),
    # Fix android.hardware.security.keymint-V1-ndk_platform dependency
    ('vendor/lib/libtpa.so', 'vendor/lib64/libtpa.so'): blob_fixup()
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so', 'android.hardware.security.keymint-V4-ndk.so')
        .replace_needed('android.hardware.security.keymint-V1-ndk.so', 'android.hardware.security.keymint-V4-ndk.so'),
    # Fix libz_stable dependency to use libz instead
    'vendor/bin/applypatch': blob_fixup()
        .replace_needed('libz_stable.so', 'libz.so'),
    # Fix keymint ndk platform dependency
    'vendor/bin/hw/android.hardware.security.keymint-service.trustonic': blob_fixup()
        .replace_needed(
            'android.hardware.security.keymint-V1-ndk_platform.so',
            'android.hardware.security.keymint-V1-ndk.so'
        )
        .replace_needed(
            'android.hardware.security.secureclock-V1-ndk_platform.so',
            'android.hardware.security.secureclock-V1-ndk.so'
        )
        .replace_needed(
            'android.hardware.security.sharedsecret-V1-ndk_platform.so',
            'android.hardware.security.sharedsecret-V1-ndk.so'
        )
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'vicky',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()