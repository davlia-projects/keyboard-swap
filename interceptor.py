import Quartz as Q
from time import time

from common import *
from analyzer import Analyzer

class Interceptor:
    def __init__(self):
        self.analyzer = Analyzer()
        event_mask = Q.CGEventMaskBit(Q.kCGEventKeyDown)
        self.tap = Q.CGEventTapCreate(Q.kCGHIDEventTap, Q.kCGHeadInsertEventTap, Q.kCGEventTapOptionDefault, event_mask, self.handler, None)
        self.loop_source = Q.CFMachPortCreateRunLoopSource(Q.kCFAllocatorDefault, self.tap, 0)
        self.event_source = Q.CGEventSourceCreate(Q.kCGEventSourceStateHIDSystemState)
        self.logs = []
        self.last_dump = time()

    def run(self):
        Q.CFRunLoopAddSource(Q.CFRunLoopGetCurrent(), self.loop_source, Q.kCFRunLoopCommonModes)
        Q.CGEventTapEnable(self.tap, True)
        Q.CFRunLoopRun()

    def handler(self, proxy, type, event, refcon):
        _, key = Q.CGEventKeyboardGetUnicodeString(event, 1, None, None)
        self.log(key)

        flag = Q.CGEventGetFlags(event)
        if flag == 1 << 8:
            self.analyzer.register(key)

        keys, layout = self.analyzer.current_keyboard()
        # print(key, layout)
        if layout == QWERTY:
            try:
                Q.CGEventKeyboardSetUnicodeString(event, 1, colemak_to_qwerty.get(key, key))
            except:
                pass
            # [self.press_key("Delete") for _ in keys]
            # [self.press_key(char, upper=char.isupper()) for char in keys]


        return event

    def press_key(self, key, upper=False):
        if upper:
            Q.CGEventPost(Q.kCGHIDEventTap, Q.CGEventCreateKeyboardEvent(self.event_source, keycodes["Shift"], True))

        Q.CGEventPost(Q.kCGHIDEventTap, Q.CGEventCreateKeyboardEvent(self.event_source, keycodes.get(key, 0x31), True))
        Q.CGEventPost(Q.kCGHIDEventTap, Q.CGEventCreateKeyboardEvent(self.event_source, keycodes.get(key, 0x31), False)) # Maybe not necessary?

        if upper:
            Q.CGEventPost(Q.kCGHIDEventTap, Q.CGEventCreateKeyboardEvent(self.event_source, keycodes["Shift"], False))


    def stop(self):
        Q.CGEventTapEnable(self.tap, False)
        Q.CFRunLoopStop(Q.CFRunLoopGetCurrent())
        Q.CFRunLoopRemoveSource(Q.CFRunLoopGetCurrent(), self.loop_source, Q.kCFRunLoopCommonModes)
        Q.CFRelease(self.tap)
        Q.CFRelease(self.loop_source)

    def log(self, key):
        self.logs.append(key)
        if len(self.logs) > MAX_LOG_LENGTH or time() - self.last_dump > 10:
            with open('log.l', 'a+') as f:
                f.write(''.join(self.logs))
                self.last_dump = time()
                self.logs = []

