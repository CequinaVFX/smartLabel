##############################################################################
'''
smartLabel
version: 1.2.0
release: October 20 2021

Created by Luciano Cequinel (vimeo.com/cequinavfx)
to report bugs or suggestions lucianocequinel@gmail.com
or linkedin.com/in/cequinel


---------------------------------------------
to install, put this file on your .nuke folder

You can find your .nuke folder at:
Linux:      /home/login name/.nuke
macOS:      /Users/login name/.nuke
Windows:    drive letter:\Users\user_name\.nuke


and copy this line on your menu.py file

import smartLabel

Toolbar = nuke.menu('Nodes')
cqnTools = Toolbar.addMenu('CQNTools', 'Modify.png')
cqnTools.addCommand('Mark all tracks', 'markAllTracks.get_Properties()', 'Shift+Q', icon = 'Text.png')
---------------------------------------------


'''
##############################################################################

import os
import nuke

def findIcon(selNode, oldLabel, oldIcon):

    '''
    icons_folder = 'C:/Program Files/Nuke11.3v1/plugins/icons/'

    path, shots, files = next(os.walk(icons_folder))

    icons = (', '.join(files))
    icons = icons.replace(',', ' ')
    '''

    iconsList = ['none', 'Add.png', 'Backdrop.png', 'Bezier.png', 'Camera.png', 'CameraTracker.png', 'ChannelMerge.png',
            'Color.png', 'ColorAdd.png', 'ColorBars.png', 'ColorCorrect.png', 'ColorLookup.png', 
            'ColorSpace.png', 'ColorWheel.png', 'CornerPin.png', 'Crop.png', 'Crosstalk.png', 'Cube.png',
            'denoise.png', 'Dot.png', 'EnvironMaps.png', 'Environment.png', 'Exposure.png', 'Expression.png',
            'FloodFill.png', 'FrameHold.png', 'FrameRange.png', 'Geometry.png', 'Glint.png', 'Glow.png', 'Histogram.png',
            'Input.png', 'Keyer.png', 'Light.png', 'MarkerRemoval.png', 'Merge.png',
            'Modify.png', 'MotionBlur2D.png', 'NoOp.png', 'Output.png', 'Paint.png',
            'Particles.png', 'Position.png', 'Precomp.png', 'Primatte.png', 'Radial.png', 'Ramp.png', 'Read.png',
            'Reformat.png', 'Render.png', 'Retime.png', 'Roto.png', 'RotoPaint.png', 'Shuffle.png', 'Sparkles.png', 'Sphere.png',
            'StickyNote.png', 'TabScriptEditor.png', 'TimeOffset.png', 'Tracker.png', 'Viewer.png', 'Write.png']

    #oldIcon = oldLabel.split('>')[1]

    #oldIcon = oldIcon.split('"')[1]

    if oldIcon in iconsList:

        ind = (iconsList.index(oldIcon))

        iconsList.pop(ind)

        icons = (', '.join(iconsList))
        icons = icons.replace(',', ' ')

        icons = oldIcon + ' ' + icons

        return (icons)

    else:
        icons = (', '.join(iconsList))
        icons = icons.replace(',', ' ')

        return (icons)


def findAlign(selNode, oldLabel, oldAlign):

    alignList = ['left', 'center', 'right']
  
    #oldAlign = oldLabel.split('>')[0]

    #oldAlign = oldAlign.replace('<', '')

    if oldAlign in alignList:

        ind = (alignList.index(oldAlign))

        alignList.pop(ind)

        align = (', '.join(alignList))
        align = align.replace(',', ' ')

        align = oldAlign + ' ' + align

        return (align)
    
    else:
        align = (', '.join(alignList))
        align = align.replace(',', ' ')

        return (align)


def getOldInfo(selNode):

    oldLabel = selNode['label'].value()

    try:
        oldAlign = oldLabel.split('>')[0]
        oldAlign = oldAlign.replace('<', '')
    except:
        oldAlign = ''

    try:
        oldIcon = oldLabel.split('>')[1]
        oldIcon = oldIcon.split('"')[1]
    except:
        oldIcon = ''

    try:
        tempOldLabel = oldLabel.split('>')[-1]
    except:
        tempOldLabel = ''

    oldSize = selNode['note_font_size'].value()

    try:
        oldOrder = selNode['z_order'].value()
    except:
        oldOrder = 1


    return (oldAlign, oldIcon, oldLabel, tempOldLabel, oldSize, oldOrder)


def infoNode(selNode, oldAlign, oldIcon, oldLabel, tempOldLabel, oldSize, oldOrder):

    # function for Sticky Note, Backdrop and Dot.

    # create a panel
    z = nuke.Panel('smartLabel...')

    z.addSingleLineInput('new label', tempOldLabel)
    z.addSingleLineInput('size', int(oldSize))

    if (selNode.Class()) == ('BackdropNode'):
        z.addSingleLineInput('order', int(oldOrder))

    if (selNode.Class()) == ('StickyNote') or (selNode.Class()) == ('BackdropNode'):
        align = findAlign(selNode, oldLabel, oldAlign)
        z.addEnumerationPulldown('align', align)

    icons = findIcon(selNode, oldLabel, oldIcon)
    z.addEnumerationPulldown('icon', icons)

    z.addBooleanCheckBox('bold', True)
    z.addBooleanCheckBox('italic', True)

    z.setWidth(600)
    result = z.show()

    # if user hits OK
    if result == True:

        newLabel = z.value('new label')
    
        try: # in case user put a letter or a float number
            newSize = int(z.value('size'))
        except:
            newSize = oldSize

        if selNode.Class() == ('BackdropNode'): # change Backdrop

            newAlign = z.value('align')
            newIcon = z.value('icon')

            newOrder = int(z.value('order'))

            bold = z.value('bold')
            italic = z.value('italic')


            selNode['note_font_size'].setValue(float(newSize))

            selNode['z_order'].setValue(newOrder)


            if newIcon == 'none':
                selNode['label'].setValue('<%s>%s' %(newAlign, newLabel))

            else:
                selNode['label'].setValue('<%s><img src = "%s">%s' %(newAlign, newIcon, newLabel))


            if bold == True and italic == True:
                selNode['note_font'].setValue('Verdana bold italic')


            elif bold == True and italic == False:
                selNode['note_font'].setValue('Verdana bold')


            elif bold == False and italic == True:
                selNode['note_font'].setValue('Verdana italic')


            else:
                selNode['note_font'].setValue('Verdana')



        elif selNode.Class() == ('StickyNote'): # change Sticky Note

            newAlign = z.value('align')
            newIcon = z.value('icon')

            bold = z.value('bold')
            italic = z.value('italic')

            selNode['note_font_size'].setValue(float(newSize))

            if newIcon == 'none':
                selNode['label'].setValue('<%s>%s' %(newAlign, newLabel))

            else:
                selNode['label'].setValue('<%s><img src = "%s">%s' %(newAlign, newIcon, newLabel))


            if bold == True and italic == True:
                selNode['note_font'].setValue('Verdana bold italic')


            elif bold == True and italic == False:
                selNode['note_font'].setValue('Verdana bold')


            elif bold == False and italic == True:
                selNode['note_font'].setValue('Verdana italic')


            else:
                selNode['note_font'].setValue('Verdana')


        else: # change Dot

            newIcon = z.value('icon')

            bold = z.value('bold')
            italic = z.value('italic')

            selNode['note_font_size'].setValue(float(newSize))

            if newIcon == 'none':
                selNode['label'].setValue('%s' %(newLabel))

            else:
                selNode['label'].setValue('<img src = "%s">%s' %(newIcon, newLabel))


            if bold == True and italic == True:
                selNode['note_font'].setValue('Verdana bold italic')


            elif bold == True and italic == False:
                selNode['note_font'].setValue('Verdana bold')


            elif bold == False and italic == True:
                selNode['note_font'].setValue('Verdana italic')


            else:
                selNode['note_font'].setValue('Verdana')


    # if user hits Cancel
    else:
        return


def mergeNode(selNode, oldLabel, oldOper, oldBBox):

    # function for Merge and Channel Merge

    # create a panel
    z = nuke.Panel('Labelizer...')

    z.addSingleLineInput('new label', oldLabel)

    # create a list to fill the dropdown with Merge's operators
    if selNode.Class() == ('Merge2'):
        
        allOperList = ['over', 'plus', 'screen', 'mask', 'multiply', 'overlay', 'from', 'stencil', 'difference', 'atop', 'average', 'color-burn',
                        'color-dodge', 'conjoint-over', 'copy', 'disjoint-over', 'divide', 'exclusion', 'geometric', 'hard-light', 'hypot', 'in',
                        'matte', 'max', 'min', 'minus', 'out', 'soft-light', 'under', 'xor']

        if oldOper in allOperList:

            ind = (allOperList.index(oldOper))

            allOperList.pop(ind)

            operList = oldOper
            
            for o in allOperList:
                operList = operList + ' ' + o

        # create a list to fill bbox dropdown
        allbboxList = ['union', 'intersection', 'A', 'B']
    
        if oldBBox in allbboxList:
    
            ind = (allbboxList.index(oldBBox))
    
            allbboxList.pop(ind)
    
            bboxList = oldBBox
            
            for o in allbboxList:
                bboxList = bboxList + ' ' + o
        else:
            bboxList = 'union intersect A B'


    # create a list to fill the dropdown with Channel Merge's operators
    elif selNode.Class() == ('ChannelMerge'):

        allOperList = ['union', 'in', 'stencil', 'minus', 'out', 'absminus', 'b-if-not-a', 'divide', 'from', 'max', 'min',  'multiply',  'plus', 'xor']

        if oldOper in allOperList:

            ind = (allOperList.index(oldOper))

            allOperList.pop(ind)

            operList = oldOper
            
            for o in allOperList:
                operList = operList + ' ' + o


        # create a list to fill bbox dropdown
        allbboxList = ['union', 'A', 'B']
    
        if oldBBox in allbboxList:
    
            ind = (allbboxList.index(oldBBox))
    
            allbboxList.pop(ind)
    
            bboxList = oldBBox
            
            for o in allbboxList:
                bboxList = bboxList + ' ' + o
        else:
            bboxList = 'union A B'


    z.addEnumerationPulldown('operation', operList)

    z.addEnumerationPulldown('bbox', bboxList)

    z.setWidth(600)
    result = z.show()

    # if user hits OK
    if result == True:

        newLabel = z.value('new label')
        newOper = z.value('operation')
        newbbox = z.value('bbox')

        selNode['label'].setValue(newLabel)
        selNode['operation'].setValue(newOper)
        selNode['bbox'].setValue(newbbox)

    # if user hits Cancel
    else:
        return


def otherNode(selNode, oldLabel):

    # function for any other node

    # create a panel
    z = nuke.Panel('Labelizer...')
    z.addSingleLineInput('new label', oldLabel)

    z.setWidth(600)
    result = z.show()

    # if user hits OK
    if result == True:
        newLabel = z.value('new label')
        selNode['label'].setValue(newLabel)

    # if user hits Cancel
    else:
        return


def smartLabel():

    # find wich node was selected and send to correct function

    selNode = nuke.selectedNodes()

    if len(selNode) == 1:

        selNode = nuke.selectedNode()

        oldAlign, oldIcon, oldLabel, tempOldLabel, oldSize, oldOrder = getOldInfo(selNode)

        if selNode.Class() in ('StickyNote', 'BackdropNode', 'Dot'): # for Sticky Note, a Backdro or a Dot

            infoNode(selNode, oldAlign, oldIcon, oldLabel, tempOldLabel, oldSize, oldOrder)

        elif selNode.Class() in ('Merge2', 'ChannelMerge'): # for Merge and Channel Merge

            oldOper = selNode['operation'].value()
            oldBBox = selNode['bbox'].value()

            mergeNode(selNode, oldLabel, oldOper, oldBBox)

        else: # for any other node
            otherNode(selNode, oldLabel)

    elif len(selNode) > 1:
        nuke.message('Select only one node...')

    else:
        nuke.message('Select something...')


if __name__ == '__main__':
    smartLabel()