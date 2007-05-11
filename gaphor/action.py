"""
Support for actions in generic files.

See also gaphor/service/actionmanager.py for the management module.
"""

class action(object):
    """
    Decorator. Turns a regular function (/method) into a full blown
    Action class.

    >>> class A(object):
    ...     @action(name="my_action", label="my action")
    ...     def myaction(self):
    ...         print 'action called'
    >>> a = A()
    >>> a.myaction()
    action called
    >>> is_action(a.myaction)
    True
    >>> for method in dir(A):
    ...     if is_action(getattr(A, method)):
    ...         print method
    myaction
    >>> A.myaction.__action__.name
    'my_action'
    >>> A.myaction.__action__.label
    'my action'
    """

    def __init__(self, name, label=None, tooltip=None, stock_id=None, accel=None, **kwargs):
        self.name = name
        self.label = label
        self.tooltip = tooltip
        self.stock_id = stock_id
        self.accel = accel
        self.__dict__.update(kwargs)

    def __call__(self, func):
        func.__action__ = self
        #for n, v in self.kwargs.items():
        #    setattr(func, n, v)
        return func
        

class toggle_action(action):
    """
    A toggle button can be switched on and off.
    An extra 'active' attribute is provided than gives the initial status.
    """
    def __init__(self, name, label=None, accel=None, active=False):
        super(toggle_action, self).__init__(name, label, accel=accel, active=active)


class radio_action(action):
    """
    Radio buttons take a list of names, a list of labels and a list of
    tooltips (and optionally, a list of stock_ids).
    The callback function should have an extra value property, which is
    given the index number of the activated radio button action.
    """
    def __init__(self, names, labels=None, tooltips=None, stock_ids=None, accels=None, active=0):
        super(radio_action, self).__init__(names[0], names=names, labels=labels, tooltips=tooltips, stock_ids=stock_ids, accels=accels, active=active)


def is_action(func):
    return bool(getattr(func, '__action__', False))


def build_action_group(obj, name=None):
    """
    Build actions and an ActionGroup for each Action instance found in obj()
    (that's why Action is a class ;) ). This function requires GTK+.

    >>> class A(object):
    ...     @action(name='bar')
    ...     def bar(self): print 'Say bar'
    ...     @toggle_action(name='foo')
    ...     def foo(self, active): print 'Say foo', active
    ...     @radio_action(names=('baz', 'beer'))
    ...     def baz(self, value):
    ...         print 'Say', value, (value and 'beer' or 'baz')
    >>> group = build_action_group(A())
    >>> len(group.list_actions())
    4
    >>> a = group.get_action('bar')
    >>> a.activate()
    Say bar
    >>> group.get_action('foo').activate()
    Say foo True
    >>> group.get_action('beer').activate()
    Say 1 beer
    >>> group.get_action('baz').activate()
    Say 0 baz
    """
    import gtk
    group = gtk.ActionGroup(name or obj)

    for attrname in dir(obj):
        try:
            method = getattr(obj, attrname)
        except:
            continue
        act = getattr(method, '__action__', None)
        if isinstance(act, radio_action):
            actgroup = None
            if not act.labels: act.labels = [None] * len(act.names)
            if not act.tooltips: act.tooltips = [None] * len(act.names)
            if not act.stock_ids: act.stock_ids = [None] * len(act.names)
            if not act.accels: act.accels = [None] * len(act.names)
            assert len(act.names) == len(act.labels)
            assert len(act.names) == len(act.tooltips)
            assert len(act.names) == len(act.stock_ids)
            assert len(act.names) == len(act.accels)
            for i, n in enumerate(act.names):
                # TODO: fix radio buttons
                
                gtkact = gtk.RadioAction(n, act.labels[i], act.tooltips[i], act.stock_ids[i], value=i)
                if act.active == i:
                    gtkact.props.active = True

                if not actgroup:
                    actgroup = gtkact
                    gtkact.connect('changed', _radio_action_changed, obj, attrname)
                else:
                    gtkact.props.group = actgroup
                group.add_action_with_accel(gtkact, act.accels[i])
        elif isinstance(act, toggle_action):
            gtkact = gtk.ToggleAction(act.name, act.label, act.tooltip, act.stock_id)
            gtkact.set_property('active', act.active)
            gtkact.connect('activate', _toggle_action_activate, obj, attrname)
            group.add_action_with_accel(gtkact, act.accel)
        elif isinstance(act, action):
            gtkact = gtk.Action(act.name, act.label, act.tooltip, act.stock_id)
            gtkact.connect('activate', _action_activate, obj, attrname)
            group.add_action_with_accel(gtkact, act.accel)
        elif act is not None:
            raise TypeError, 'Invalid action type: %s' % action
    return group


def _action_activate(action, obj, name):
    method = getattr(obj, name)
    method()


def _toggle_action_activate(action, obj, name):
    method = getattr(obj, name)
    method(action.props.active)


def _radio_action_changed(action, current_action, obj, name):
    method = getattr(obj, name)
    method(current_action.props.value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

# vim:sw=4:et:ai
