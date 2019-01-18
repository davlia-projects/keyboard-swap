from Foundation import NSObject
from AppKit import NSApplication, NSApp
from Cocoa import (NSEvent, NSEventMaskKeyDown, NSEventMaskKeyUp, NSKeyUp)
import Quartz as Q
from PyObjCTools import AppHelper
import signal
from lockfile import LockFile

class Sniffer:
    def __init__(self):
        self.lock = LockFile("switch.pid")
        if self.lock.is_locked():
            print("well shit")
            exit(1)
        # self.lock.acquire()

    def createAppDelegate(self):
        sc = self

        class AppDelegate(NSObject):

            def applicationDidFinishLaunching_(self, notification):
                mask = NSEventMaskKeyDown | NSEventMaskKeyUp
                NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, sc.handler)

            def applicationWillResignActive(self):
                self.applicationWillTerminate_(None)
                return True

            def applicationShouldTerminate_(self, notification):
                self.applicationWillTerminate_(notification)
                return True

            def applicationWillTerminate_(self, notification):
                if sc.lock.is_locked():
                    sc.lock.release()

        return AppDelegate

    def run(self):
        NSApplication.sharedApplication()
        delegate = self.createAppDelegate().alloc().init()
        NSApp().setDelegate_(delegate)
        signal.signal(signal.SIGINT, lambda signal, frame: AppHelper.stopEventLoop())
        AppHelper.runEventLoop()

    def handler(self, event):
        try:
            event_type = event.type()
            if event_type == NSKeyUp:
                print("Pressed %s" % event.charactersIgnoringModifiers())
        except:
            AppHelper.stopEventLoop()
            raise
