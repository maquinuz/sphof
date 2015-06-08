#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import tkinter
import threading
from random import randint
from PIL import Image, ImageDraw, ImageTk
from zocp import ZOCP
from sys import getrefcount as grc
import ctypes
logger = logging.getLogger(__name__)

"""
.. module:: canvas_actors
   :platform: Unix, Windows
   :synopsis: A module for drawing on a canvas using ZOCP.

.. moduleauthor:: Arnaud Loonstra <arnaud@sphaero.org>
"""

class LazyCanvasActor(ZOCP):

    """We use this as a public class example class.

    You never call this class before calling :func:`public_fn_with_sphinxy_docstring`.

    .. note::

       An example of intersphinx is this: you **cannot** use :mod:`pickle` on this class.

    """
    def __init__(self, *args, **kwargs):
        super(LazyCanvasActor, self).__init__(*args, **kwargs)
        if kwargs.get("imagefile"):
            self._img = Image.open(kwargs.get("imagefile"))
        else:
            self._img = Image.new("RGB", (200,600), (255,255,55))
        self._d = ImageDraw.Draw(self._img)

        self._display = tkinter.Tk()
        self.canvas = tkinter.Canvas(self._display, width=200, height=600)
        self.canvas.pack()
        #self.canvas.image = ImageTk.PhotoImage(self._img)
        #self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self._display.bind("<Button>", self._button_click_exit_mainloop)
        #self.canvas.image = ImageTk.PhotoImage(self._img)
 
        self.start()
        self.setup()
        self._loop()

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

    def update(self):
        """
        Called every loop
        """
        logger.warning("Please implement an update method!!!")

    def draw(self):
        """
        Called after update to draw the canvas on screen
        """
        self.canvas.image1 = ImageTk.PhotoImage(self._img)
        self.canvas.create_image(0, 0, image=self.canvas.image1, anchor='nw')
        self._display.update()

    def reset(self):
        """
        Clears the image to the background color
        """
        self._img = Image.new("RGB", (200,600), self.background_color)
        self._d = ImageDraw.Draw(self._img)

    def get_width(self):
        """
        Returns the width of the canvas
        """
        return 200

    def get_height(self):
        """
        Returns the height of the canvas
        """
        return 600


    def arc(self, *args, **kwargs):
        """
        Draws an arc (a portion of a circle outline) between the start and end
        angles, inside the given bounding box.

        :param xy: Four points to define the bounding box. Sequence of
            ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param start: Starting angle, in degrees. Angles are measured from
                3 o'clock, increasing clockwise.
        :param end: Ending angle, in degrees.
        :param fill: Color to use for the arc.
        """
        self._d.arc(*args, **kwargs)

    def bitmap(self, *args, **kwargs):
        """        
        Draws a bitmap (mask) at the given position, using the current fill color
        for the non-zero portions. The bitmap should be a valid transparency mask
        (mode “1”) or matte (mode “L” or “RGBA”).

        This is equivalent to doing ``image.paste(xy, color, bitmap)``.

        To paste pixel data into an image, use the
        :py:meth:`~PIL.Image.Image.paste` method on the image itself.
        """
        self._d.bitmap(*args, **kwargs)

    def chord(self, *args, **kwargs):
        """
        Same as :py:meth:`~PIL.ImageDraw.Draw.arc`, but connects the end points
        with a straight line.

        :param xy: Four points to define the bounding box. Sequence of
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.
        """
        self._d.chord(*args, **kwargs)

    def ellipse(self, *args, **kwargs):
        """
        Draws an ellipse inside the given bounding box.

        :param xy: Four points to define the bounding box. Sequence of either
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.
        """
        self._d.ellipse(*args, **kwargs)

    def line(self, *args, **kwargs):
        """
        Draws a line between the coordinates in the **xy** list.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param fill: Color to use for the line.
        :param width: The line width, in pixels. Note that line
               joins are not handled well, so wide polylines will not look good.        
        """
        self._d.line(*args, **kwargs)

    def pieslice(self, *args, **kwargs):
        """
        Same as arc, but also draws straight lines between the end points and the
        center of the bounding box.

        :param xy: Four points to define the bounding box. Sequence of
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param start: Starting angle, in degrees. Angles are measured from
                3 o'clock, increasing clockwise.
        :param end: Ending angle, in degrees.
        :param fill: Color to use for the fill.
        :param outline: Color to use for the outline.        
        """
        self._d.pieslice(*args, **kwargs)

    def point(self, *args, **kwargs):
        """
        Draws points (individual pixels) at the given coordinates.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param fill: Color to use for the point.        
        """
        self._d.point(*args, **kwargs)

    def polygon(self, *args, **kwargs):
        """ 
        Draws a polygon.

        The polygon outline consists of straight lines between the given
        coordinates, plus a straight line between the last and the first
        coordinate.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.       
        """
        self._d.polygon(*args, **kwargs)

    def rectangle(self, *args, **kwargs):
        """
         Draws a rectangle.

        :param xy: Four points to define the bounding box. Sequence of either
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``. The second point
                is just outside the drawn rectangle.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.       
        """
        self._d.rectangle(self, *args, **kwargs)

    def text(self, *args, **kwargs):
        """
        Draws the string at the given position.

        :param xy: Top left corner of the text.
        :param text: Text to be drawn.
        :param font: An :py:class:`~PIL.ImageFont.ImageFont` instance.
        :param fill: Color to use for the text.        
        """
        self._d.text(*args, **kwargs)
    
    def textsize(self, *args, **kwargs):
        """
        Return the size of the given string, in pixels.

        :param text: Text to be measured.
        :param font: An :py:class:`~PIL.ImageFont.ImageFont` instance.        
        """
        self._d.textsize(*args, **kwargs)

    def _button_click_exit_mainloop (event):
        event.widget.quit() # this will cause mainloop to unblock.

    def _loop(self):
        self._running = True
        count = 0
        t = time.time()
        try:
            reap_at = time.time() + 1/60.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                self.run_once(0) #timeout * 1000)
                reap_at = time.time() + 1/60.

                self.update()
                self.draw()
                count += 1
                if t + 60 < time.time():
                    print("{0}: fps: {1}".format(self.name, count/((time.time() - t))))
                    t = time.time()
                    count = 0
        except Exception as e:
            print(e)
        finally:
            self.stop()

class CanvasActor(ZOCP):

    """Canvas Actor class, threaded version.

    .. note::

       An example of intersphinx is this: you **cannot** use :mod:`pickle` on this class.

    """

    def __init__(self, *args, **kwargs):
        super(CanvasActor, self).__init__(*args, **kwargs)

        self._count = 0  #fps counter
        self._img = None
        self._oldimg = {} #[None]*10
        self.background_color = (15,15,15)
        self.setup()
        self.reset()
        
        self.register_int("imgId", id(self._img), 're')
        self.register_int("rmId", 0, 'rs')

        self.start()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

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

    def update(self):
        """
        Called every loop
        """
        logger.warning("Please implement an update method!!!")

    def reset(self):
        """
        Clears the image to the background color
        """
        self._img = Image.new("RGB", (200,600), self.background_color)
        self._d = ImageDraw.Draw(self._img)

    def send_img(self):
        """
        Sends the image as a signal to any subscribers
        """
        self.emit_signal("imgId", id(self._img))

    def get_width(self):
        """
        Returns the width of the canvas
        """
        return 200

    def get_height(self):
        """
        Returns the height of the canvas
        """
        return 600

    def arc(self, *args, **kwargs):
        """
        Draws an arc (a portion of a circle outline) between the start and end
        angles, inside the given bounding box.

        :param xy: Four points to define the bounding box. Sequence of
            ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param start: Starting angle, in degrees. Angles are measured from
                3 o'clock, increasing clockwise.
        :param end: Ending angle, in degrees.
        :param fill: Color to use for the arc.
        """
        self._d.arc(*args, **kwargs)

    def bitmap(self, *args, **kwargs):
        """        
        Draws a bitmap (mask) at the given position, using the current fill color
        for the non-zero portions. The bitmap should be a valid transparency mask
        (mode “1”) or matte (mode “L” or “RGBA”).

        This is equivalent to doing ``image.paste(xy, color, bitmap)``.

        To paste pixel data into an image, use the
        :py:meth:`~PIL.Image.Image.paste` method on the image itself.
        """
        self._d.bitmap(*args, **kwargs)

    def chord(self, *args, **kwargs):
        """
        Same as :py:meth:`~PIL.ImageDraw.Draw.arc`, but connects the end points
        with a straight line.

        :param xy: Four points to define the bounding box. Sequence of
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.
        """
        self._d.chord(*args, **kwargs)

    def ellipse(self, *args, **kwargs):
        """
        Draws an ellipse inside the given bounding box.

        :param xy: Four points to define the bounding box. Sequence of either
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.
        """
        self._d.ellipse(*args, **kwargs)

    def line(self, *args, **kwargs):
        """
        Draws a line between the coordinates in the **xy** list.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param fill: Color to use for the line.
        :param width: The line width, in pixels. Note that line
            joins are not handled well, so wide polylines will not look good.        
        """
        self._d.line(*args, **kwargs)

    def pieslice(self, *args, **kwargs):
        """
        Same as arc, but also draws straight lines between the end points and the
        center of the bounding box.

        :param xy: Four points to define the bounding box. Sequence of
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param start: Starting angle, in degrees. Angles are measured from
                3 o'clock, increasing clockwise.
        :param end: Ending angle, in degrees.
        :param fill: Color to use for the fill.
        :param outline: Color to use for the outline.        
        """
        self._d.pieslice(*args, **kwargs)

    def point(self, *args, **kwargs):
        """
        Draws points (individual pixels) at the given coordinates.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param fill: Color to use for the point.        
        """
        self._d.point(*args, **kwargs)

    def polygon(self, *args, **kwargs):
        """ 
        Draws a polygon.

        The polygon outline consists of straight lines between the given
        coordinates, plus a straight line between the last and the first
        coordinate.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.       
        """
        self._d.polygon(*args, **kwargs)

    def rectangle(self, *args, **kwargs):
        """
         Draws a rectangle.

        :param xy: Four points to define the bounding box. Sequence of either
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``. The second point
                is just outside the drawn rectangle.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.       
        """
        self._d.rectangle(self, *args, **kwargs)

    def text(self, *args, **kwargs):
        """
        Draws the string at the given position.

        :param xy: Top left corner of the text.
        :param text: Text to be drawn.
        :param font: An :py:class:`~PIL.ImageFont.ImageFont` instance.
        :param fill: Color to use for the text.        
        """
        self._d.text(*args, **kwargs)
    
    def textsize(self, *args, **kwargs):
        """
        Return the size of the given string, in pixels.

        :param text: Text to be measured.
        :param font: An :py:class:`~PIL.ImageFont.ImageFont` instance.        
        """
        self._d.textsize(*args, **kwargs)

    def on_peer_subscribed(self, peer, name, data, *args, **kwargs):
        self.send_img()

    def on_peer_signaled(self, peer, name, data, *args, **kwargs):
        #logger.warning("CANVAS PEER SIGNALED: %s modified %s" %(name, data))
        if name == "Painter":
            imgID = data[1]
            if imgID in self._oldimg.keys():
                # remove img if peer signals it has received it
                b = self._oldimg.pop(imgID, 0)
                assert(b != 0)
                #b.close()
                #del(b)
                #print("BOE:", len(self._oldimg))
            # keep refs to prevent gc
            self._oldimg[id(self._img)] = self._img
            self.send_img()
            self.reset()

    def _button_click_exit_mainloop (event):
        event.widget.quit() # this will cause mainloop to unblock.
        self.stop()

    def _pre_update(self):
        self._count += 1
        
    def _post_update(self):
        pass

    def run(self):
        self._running = True
        t = time.time()
        try:
            reap_at = time.time() + 1/120.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                self.run_once(timeout * 1000)
                # set next interval
                reap_at = time.time() + 1/120.
 
                self._pre_update()
                self.update()
                self._post_update()
 
                # stats
                if t + 1 < time.time():
                    print("{0}: fps: {1}".format(self.name(), 1/((time.time() - t)/self._count)))
                    t = time.time()
                    self._count = 0
        except KeyboardInterrupt as e:
            print("Exception: ZCanvas_t:{0}".format(e))
        finally:
            self._running = False
            self.stop()


if __name__ == '__main__':
    test1 = ZCanvas_t("Thread1")
    test2 = ZCanvas_t("Thread2")
    try:
        test1.thread.join()
        test2.thread.join()
    except Exception as e:
        print(e)
    finally:
        test1.stop()
        test2.stop()
        print("FINISHED")
    
    # Normal Actor
    #test = ZCanvas("TEST")
