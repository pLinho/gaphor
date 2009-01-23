"""
Message item connection adapters.
"""

from gaphor.adapters.connectors import AbstractConnect
from zope import interface, component
from gaphor import UML
from gaphor.diagram import items

class MessageLifelineConnect(AbstractConnect):
    """
    Connect lifeline with a message.

    A message can connect to both the lifeline's head (the rectangle)
    or the lifetime line. In case it's added to the head, the message
    is considered to be part of a communication diagram. If the message is
    added to a lifetime line, it's considered a sequence diagram.
    """

    component.adapts(items.LifelineItem, items.MessageItem)

    def connect_lifelines(self, line, send, received):
        """
        Always create a new Message with two EventOccurence instances.
        """
        def get_subject():
            if not line.subject:
                message = self.element_factory.create(UML.Message)
                message.name = 'call()'
                line.subject = message
            return line.subject

        if send:
            message = get_subject()
            if not message.sendEvent:
                event = self.element_factory.create(UML.EventOccurrence)
                event.sendMessage = message
                event.covered = send.subject

        if received:
            message = get_subject()
            if not message.receiveEvent:
                event = self.element_factory.create(UML.EventOccurrence)
                event.receiveMessage = message
                event.covered = received.subject


    def disconnect_lifelines(self, line):
        """
        Disconnect lifeline and set appropriate kind of message item. If
        there are no lifelines connected on both ends, then remove the message
        from the data model.
        """
        send = line.head.connected_to
        received = line.tail.connected_to

        if send:
            event = line.subject.receiveEvent
            if event:
                event.unlink()

        if received:
            event = line.subject.sendEvent
            if event:
                event.unlink()

        # one is disconnected and one is about to be disconnected,
        # so destroy the message
        if not send or not received:
            # Both ends are disconnected:
            message = line.subject
            del line.subject
            if not message.presentation:
                message.unlink()
            for message in list(line._messages):
                line.remove_message(message, False)
                message.unlink()

            for message in list(line._inverted_messages):
                line.remove_message(message, True)
                message.unlink()


    def glue(self, handle, port):
        """
        Glue to lifeline's head or lifetime. If lifeline's lifetime is
        visible then disallow connection to lifeline's head.
        """
        element = self.element
        lifetime = element.lifetime
        line = self.line
        opposite = line.opposite(handle)

        if opposite.connected_to:
            opposite_is_visible = opposite.connected_to.lifetime.visible
            # connect lifetimes if both are visible or both invisible
            return not (lifetime.visible ^ opposite_is_visible)

        return not (lifetime.visible ^ (port is element.lifetime.port))
        

    def connect(self, handle, port):
        super(MessageLifelineConnect, self).connect(handle, port)

        line = self.line
        send = line.head.connected_to
        received = line.tail.connected_to
        self.connect_lifelines(line, send, received)

        lifetime = self.element.lifetime
        # if connected to head, then make lifetime invisible
        if port is lifetime.port:
            lifetime.min_length = lifetime.MIN_LENGTH_VISIBLE
        else:
            lifetime.visible = False
            lifetime.connectable = False


    def disconnect(self, handle):
        super(MessageLifelineConnect, self).disconnect(handle)

        line = self.line
        send = line.head.connected_to
        received = line.tail.connected_to
        lifeline = self.element
        lifetime = lifeline.lifetime

        # if a message is delete message, then disconnection causes
        # lifeline to be no longer destroyed (note that there can be
        # only one delete message connected to lifeline)
        if received and line.subject.messageSort == 'deleteMessage':
            received.is_destroyed = False
            received.request_update()

        self.disconnect_lifelines(line)

        if len(line.canvas.get_connected_items(lifeline)) == 1:
            # after disconnection count of connected items will be
            # zero, so allow connections to lifeline's lifetime
            lifetime.connectable = True
            lifetime.min_length = lifetime.MIN_LENGTH
            


component.provideAdapter(MessageLifelineConnect)

