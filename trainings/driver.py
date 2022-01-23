
import vgamepad as vg
import DirectKey as DirectKey
import keyboard

KEY_UP = 0xC8
KEY_DOWN = 0xD0
KEY_LEFT = 0xCB
KEY_RIGHT = 0xCD
RELOAD = 0x1C
REPLAYR = 0x13
REPLAYP = 0x19


def reloadKey():
    return DirectKey.HoldKey(RELOAD)


def test():
    return 0


def releaseAllKeys():
    DirectKey.ReleaseKey(KEY_UP)
    DirectKey.ReleaseKey(KEY_RIGHT)
    DirectKey.ReleaseKey(KEY_DOWN)
    DirectKey.ReleaseKey(KEY_LEFT)


def controlKey(arr):
    # out=[0,0,0,0]
    # up , right , down , left
    # 0      1      2      3
    if(arr[3]):
        DirectKey.PressKey(KEY_LEFT)
    else:
        DirectKey.ReleaseKey(KEY_LEFT)

    if(arr[2]):
        DirectKey.PressKey(KEY_DOWN)
    else:
        DirectKey.ReleaseKey(KEY_DOWN)

    if(arr[1]):
        DirectKey.PressKey(KEY_RIGHT)
    else:
        DirectKey.ReleaseKey(KEY_RIGHT)

    if(arr[0]):
        DirectKey.PressKey(KEY_UP)
    else:
        DirectKey.ReleaseKey(KEY_UP)


def controlKeySimple(val):
    # up , right , down , left
    # 0      1      2      3
    releaseAllKeys()
    if(val == 0):
        DirectKey.PressKey(KEY_UP)
    elif(val == 1):
        DirectKey.PressKey(KEY_RIGHT)
    elif(val == 2):
        DirectKey.PressKey(KEY_DOWN)
    elif(val == 3):
        DirectKey.PressKey(KEY_LEFT)
    else:
        pass


def controlKeyDumb(val):
    # up , down
    # 0      1
    releaseAllKeys()
    if(val == 0):
        DirectKey.PressKey(KEY_UP)
    elif(val == 1):
        DirectKey.PressKey(KEY_DOWN)
    else:
        pass


def controlKeySmooth(val):
    # left left/up  up   right/up right
    # 0      1      2      3       4
    # print("test")
    # if(val == None):
    #     return
    releaseAllKeys()
    if(val == 0):
        DirectKey.PressKey(KEY_DOWN)
    elif(val == 1):
        DirectKey.PressKey(KEY_LEFT)
        DirectKey.PressKey(KEY_UP)
    elif(val == 2):
        DirectKey.PressKey(KEY_UP)
    elif(val == 3):
        DirectKey.PressKey(KEY_RIGHT)
        DirectKey.PressKey(KEY_UP)
    elif(val == 4):
        DirectKey.PressKey(KEY_RIGHT)
    elif(val == 5):
        DirectKey.PressKey(KEY_LEFT)
    else:
        pass


def saveReplay():
    releaseAllKeys()
    DirectKey.HoldKey(REPLAYP)
    DirectKey.HoldKey(KEY_UP)
    DirectKey.HoldKey(KEY_UP)
    DirectKey.HoldKey(KEY_DOWN)
    # DirectKey.HoldKey(REPLAY)
    DirectKey.HoldKey(KEY_DOWN)
    DirectKey.HoldKey(RELOAD)
    DirectKey.HoldKey(RELOAD)


def saveReplay2():
    releaseAllKeys()
    DirectKey.HoldKey(KEY_DOWN)
    DirectKey.HoldKey(RELOAD)


def controlGamepad(gamepad, control):
    #assert all(-1.0 <= c <= 1.0 for c in control), "This function accepts only controls between -1.0 and 1.0"
    if control[0] > 0:  # gas
        gamepad.right_trigger_float(value_float=control[0])
    else:
        gamepad.right_trigger_float(value_float=0.0)
    if control[1] > 0:  # break
        gamepad.left_trigger_float(value_float=control[1])
    else:
        gamepad.left_trigger_float(value_float=0.0)
    #ATTENTION *2 -1
    gamepad.left_joystick_float(control[2]*2-1, 0.0)  # turn
    gamepad.update()


def releaseGamepad(gamepad):
    gamepad.right_trigger_float(value_float=0.0)
    gamepad.left_trigger_float(value_float=0.0)
    gamepad.left_joystick_float(0.0, 0.0)

# def getInput():
#     if(keyboard.is_pressed("up")):
#         return 0

#     if(keyboard.is_pressed("right")):
#         return 1

#     if(keyboard.is_pressed("down")):
#         return 2

#     if(keyboard.is_pressed("left")):
#         return 3
