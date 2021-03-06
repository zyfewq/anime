import math
from types import MethodType


def linear(cur, dest, speed):
    if cur < dest:
        if cur + speed > dest:
            return dest, speed
        return cur + speed, speed
    else:
        if cur - speed < dest:
            return dest, speed
        return cur - speed, speed


def freeze(cur, dest, speed):
    """Adding this filter will simply freeze the current value and speed of
    the object"""
    return cur, speed


def spring(cur, dest, speed, k=0.2, b=0.5):
    # for animations, destX is really spring length (spring at rest). initial
    # position is considered as the stretched/compressed posiiton of a spring
    force = -k * (cur - dest)

    # Damping constant
    damper = -b * speed

    # usually we put mass here, but for animation purposes, specifying mass is a
    # bit redundant. you could simply adjust k and b accordingly
    # let a = (force + damper) / mass
    a = force + damper

    new_cur = cur + speed
    new_speed = speed + a

    return new_cur, new_speed


def bounce(cur, dest, speed, k=0.02, b=0.12):
    # for animations, destX is really spring length (spring at rest). initial
    # position is considered as the stretched/compressed posiiton of a spring
    force = -k * (cur - dest)

    # Damping constant
    damper = -b * speed

    # usually we put mass here, but for animation purposes, specifying mass is a
    # bit redundant. you could simply adjust k and b accordingly
    # let a = (force + damper) / mass
    a = force + damper

    new_cur = cur + speed
    new_speed = speed + a
    if (cur-dest >= 0) ^ (new_cur-dest >= 0): # check to see if the signs ==
        new_speed = -new_speed
        if dest-new_cur < 0:
            new_cur = dest-abs(new_cur-dest)
        else:
            new_cur = dest+abs(new_cur-dest)

    return new_cur, new_speed


def exponential(cur, dest, speed, growth=1, start=0):
    if cur < dest:
        if cur + speed > dest:
            return dest, start
        return cur + speed, speed+growth
    else:
        if cur - speed < dest:
            return dest, start
        return cur - speed, speed+growth


def done_almost_equal(cur, dest, speed, ndigits=3):
    return round(cur, ndigits) == round(dest, ndigits)


def done_speed_dest(cur, dest, speed):
    return abs(speed) < 5 and abs(cur-dest) < 5


def done_bounds(cur, dest, speed, min_, max_):
    return cur < min_ or cur > max_


class Filter(object):
    """Takes current, destination, speed"""

    def __init__(self, call=None, done=None, speed=0):
        if call: self.call = call
        if done: self.done = done
        self.speed = speed

    def __call__(self, cur, dest, speed):
        """Functions return the new value"""
        return self.call(cur, dest, speed)

    def call(self, cur, dest, speed):
        return dest, speed

    def done(self, cur, dest, speed):
        return cur == dest


class Linear(Filter):

    def __init__(self, speed):
        super().__init__(linear, None, speed)


class Freeze(Filter):

    def __init__(self):
        super().__init__(freeze, None, 0)


class Spring(Filter):

    def __init__(self, k, b):
        super().__init__(None, done_speed_dest)
        self.k = k
        self.b = b

    def call(self, cur, dest, speed):
        return spring(cur, dest, speed, self.k, self.b)


class Bounce(Filter):

    def __init__(self, k, b):
        super().__init__(None, done_speed_dest)
        self.k = k
        self.b = b

    def call(self, cur, dest, speed):
        return bounce(cur, dest, speed, self.k, self.b)


class Exponetial(Filter):

    def __init__(self, growth, start):
        super().__init__(None, None)
        self.growth = growth
        self.start = start

    def call(self, cur, dest, speed):
        return exponential(cur, dest, speed, self.growth, self.start)