#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/motorola/vicky/device.mk)

# Inherit some common LineageOS stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

BOARD_VENDOR := motorola
PRODUCT_NAME := lineage_vicky
PRODUCT_DEVICE := vicky
PRODUCT_MANUFACTURER := motorola
PRODUCT_BRAND := motorola
PRODUCT_MODEL := Moto G72

PRODUCT_GMS_CLIENTID_BASE := android-transsion

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="vicky_g_sys-user 13 T2SVS33M.68-21-6-16 e575f0 release-keys" \
    BuildFingerprint=motorola/vicky_g_sys/vicky:13/T2SVS33M.68-21-6-16/e575f0:user/release-keys

# Time
LINEAGE_VERSION_APPEND_TIME_OF_DAY := true
