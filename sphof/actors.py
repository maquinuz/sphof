#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import threading
from zocp import ZOCP

logger = logging.getLogger(__name__)

"""
Package Example (:mod:`actors`)
==================================

.. currentmodule:: actors
.. autosummary::
   :toctree:

   LoneActor
   Actor
   LeadActor
"""

class LoneActor(object):
    """
    The LoneActor class runs an application loop.
    
    By default the LoneActor loop runs at 60 iterations per second. This 
    means your update and draw method is called every 1/60th second.
    
    * Use the :py:meth:`.LoneActor.setup` method to setup the class
    * Use :py:meth:`.LoneActor.update` method to update anything you\
    have setup
    * Use :py:meth:`.LoneActor.draw` method to visualise
    """    
    def __init__(self):
        self.setup()
        
    def setup(self):
        """
        Called a startup.
        
        Add variables here
        i.e.::

            self.count = 0

        and in update()::

            count += 1

        """
        logger.warning("Please implement a setup method!!!")
    
    def update():
        """
        Called every loop
        """
        logger.warning("Please implement an update method!!!")

    def draw():
        """
        Called after update
        """
        logger.warning("Please implement a draw method!!!")

    def run(self):
        self._running = True
        count = 0
        t = time.time()
        try:
            reap_at = time.time() + 1/60.
            while self._running:
                self.update()
                timeout = reap_at - time.time()
                if timeout > 0:
                    #timeout = 0
                    time.sleep(timeout)
                else:
                    log.debug("Can't do 60 fps")
                #self.run_once(0) #timeout * 1000)
                reap_at = time.time() + 1/60.
                self.draw()
                count += 1
                if t + 60 < time.time():
                    print("{0}: fps: {1}".format(self.name(), (time.time() - t)/count))
                    t = time.time()
                    count = 0
        except (KeyboardInterrupt, SystemExit) as e:
            print(e)

class Actor(ZOCP):
    """
    An Actor class runs inside its own thread. It's usually started
    by a LeadActor!
    
    By default the Actor loop runs at 60 iterations per second. This 
    means your update and draw method is called every 1/60th second.
    
    * Use the :py:meth:`.Actor.setup` method to setup the class
    * Use :py:meth:`.Actor.update` method to update anything you\
    have setup
    * Use :py:meth:`.Actor.draw` method to visualise
    
    .. warning::
        It is important to understand that you cannot visualise directly
        from an Actor. To visualise what an actor draws you'll need to 
        handover the image to a :py:class:`LeadActor`
    """
    def __init__(self, *args, **kwargs):
        super(Actor, self).__init__(*args, **kwargs)
        self.setup()
        self.start()
    
    def setup(self):
        """
        Called a startup. 
        
        Add variables here
        i.e.::

            self.count = 0
            self.start()

        and in update()::

            self.count += 1

        """
        logger.warning("Please implement a setup method!!!")

    def start(self):
        ZOCP.start(self)                            # Start ZOCP        
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()                         # And run loop

    def pre_update(self):
        return
    
    def update(self):
        """
        Called every loop
        """
        logger.warning("Please implement an update method!!!")

    def post_update(self):
        return

    def pre_draw(self):
        return
        
    def draw(self):
        """
        Called after update
        """
        logger.warning("Please implement a draw method!!!")
    
    def post_draw(self):
        return
        
    def run(self):
        self._running = True
        t = time.time()
        count = 1
        try:
            reap_at = time.time() + 1/60.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                # set next interval
                reap_at = time.time() + 1/60.
                self.run_once(timeout * 1000)   # parse ZOCP queue

                self.pre_update()
                self.update()
                self.post_update()

                self.pre_draw()
                self.draw()
                self.post_draw()
 
                # stats
                if t + 60 < time.time():
                    print("{0}: fps: {1}".format(self.name(), (time.time() - t)/count))
                    t = time.time()
                    count = 1

        except (KeyboardInterrupt, SystemExit) as e:
            logger.warning("Actor {0} finished. Exception:{1}".format(self.name(), e))
        finally:
            self._running = False
            self.stop()
        logger.warning("Actor {0} finished.".format(self.name()))

class LeadActor(Actor):
    """
    A LeadActor class runs in the main thread. It inherits all methods 
    from the Actor class but has some additional methods to start Actors 
    
    By default the LeadActor loop runs at 60 iterations per second. This 
    means your update and draw method is called every 1/60th second.
    
    * Use the :py:meth:`.Actor.setup` method to setup the class
    * Use :py:meth:`.Actor.update` method to update anything you\
    have setup
    * Use :py:meth:`.Actor.draw` method to visualise
    """
    
    def __init__(self, *args, **kwargs):
        self.actors = []
        super(LeadActor, self).__init__(*args, **kwargs)
    
    def start(self):
        ZOCP.start(self)

    def stop(self):
        # stop all actors
        for act in self.actors:
            act.stop()
        # call our original stop method
        Actor.stop(self)
