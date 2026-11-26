/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#define LOG_TAG "android.hardware.gnss-service.mediatek"

#include <android/binder_process.h>
#include <dlfcn.h>
#include <log/log.h>

namespace {
constexpr const char* kGnssImplLib = "/vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so";
constexpr const char* kAidlGnssMainSym = "_ZN4aidl7android8hardware4gnss14aidl_gnss_mainEv";
using AidlGnssMainFn = void (*)();
}  // namespace

int main() {
    ABinderProcess_setThreadPoolMaxThreadCount(1);
    ABinderProcess_startThreadPool();

    void* handle = dlopen(kGnssImplLib, RTLD_NOW);
    if (!handle) {
        ALOGE("Failed to dlopen %s: %s", kGnssImplLib, dlerror());
        return 1;
    }

    auto aidl_gnss_main = reinterpret_cast<AidlGnssMainFn>(dlsym(handle, kAidlGnssMainSym));
    if (!aidl_gnss_main) {
        ALOGE("Failed to resolve %s: %s", kAidlGnssMainSym, dlerror());
        dlclose(handle);
        return 1;
    }

    ALOGI("Registering AIDL v1 GNSS HAL service");
    aidl_gnss_main();

    ABinderProcess_joinThreadPool();
    return 0;
}
