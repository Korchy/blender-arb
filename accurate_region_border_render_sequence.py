# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

import functools
import os
import tempfile
import bpy
from bpy.app.handlers import render_complete, render_cancel
from . import accurate_region_border_keymap


class RenderSequence:

    _render_in_progress = False
    _context = None
    _force_cancel_render = False

    @classmethod
    def render(cls, context):
        # render timeline sequence
        cls._force_cancel_render = False
        accurate_region_border_keymap.register()
        cls._context = context
        context.scene.frame_set(context.scene.frame_start)
        cls._render_current_frame(context=context)

    @classmethod
    def _render_next_frame(cls, context):
        # render next frame
        if cls._force_cancel_render:
            cls._clear()
        elif context.scene.frame_current < context.scene.frame_end:
            context.scene.frame_set(context.scene.frame_current + 1)
            cls._render_current_frame(context=context)
        else:
            cls._clear()

    @classmethod
    def _render_current_frame(cls, context):
        # start render current frame
        if cls._on_render_finish not in render_complete:
            render_complete.append(cls._on_render_finish)
        if cls._on_render_cancel not in render_cancel:
            render_cancel.append(cls._on_render_cancel)
        # execute render for current frame
        bpy.app.timers.register(functools.partial(cls._exec_render), first_interval=1.0)

    @classmethod
    def _exec_render(cls):
        # execute render
        rez = {'CANCELLED'}
        if not cls._render_in_progress:
            cls._render_in_progress = True
            rez = bpy.ops.render.render(use_viewport=True)
        if rez == {'CANCELLED'}:
            # retry with timer
            return 1.0
        else:
            return None

    @classmethod
    def _on_render_finish(cls, scene, unknown):
        # on render finish
        cls._save_image(scene=scene)
        cls._render_in_progress = False
        # render next frame
        cls._render_next_frame(context=bpy.context)

    @classmethod
    def _on_render_cancel(cls):
        # on render cancel
        cls._clear()

    @classmethod
    def _save_image(cls, scene):
        # save image from current render
        dest_dir = cls._dest_dir(
            path=scene.render.filepath
        )
        if dest_dir:
            if not os.path.isdir(dest_dir):
                os.mkdir(dest_dir)
            file_name = str(scene.frame_current).zfill(4) + scene.render.file_extension
            file_path = os.path.join(dest_dir, file_name)
            bpy.data.images['Render Result'].save_render(filepath=file_path)

    @staticmethod
    def _dest_dir(path):
        # returns absolute file path from path
        if not path:
            path = tempfile.gettempdir()
        if path[:2] == '//':
            return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), path[2:]))
        else:
            return os.path.abspath(path)

    @classmethod
    def cancel_render(cls):
        # force cancel render
        cls._force_cancel_render = True

    @classmethod
    def _clear(cls):
        cls._context = None
        cls._render_in_progress = False
        cls._force_cancel_render = False
        accurate_region_border_keymap.unregister()
        if cls._on_render_finish in render_complete:
            render_complete.remove(cls._on_render_finish)
        if cls._on_render_cancel in render_cancel:
            render_cancel.remove(cls._on_render_cancel)
