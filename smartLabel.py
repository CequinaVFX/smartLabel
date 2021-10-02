##############################################################################
'''
smartLabel
version: 1.0.0
release: October 02 2021

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


def smartLabel():

    # find wich node was selected and send to correct function

    selNode = nuke.selectedNodes()

    if len(selNode) == 1:

        selNode = nuke.selectedNode()

        oldLabel = selNode['label'].getValue()
        oldSize = selNode['note_font_size'].getValue()

        try:
            oldOrder = selNode['z_order'].value()
        except:
            oldOrder = 1


        if selNode.Class() in ('StickyNote', 'BackdropNode', 'Dot'): # for Sticky Note, a Backdro or a Dot

            try:
                align, oldLabel = oldLabel.split('>')
            except:
                pass

            infoNode(selNode, oldLabel, oldSize, oldOrder)

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


def infoNode(selNode, oldLabel, oldSize, oldOrder):

    # function for Sticky Note, Backdrop and Dot.


    icon_folder = 'C:/Program Files/Nuke11.3v1/plugins/icons/'

    path, shots, files = next(os.walk(icon_folder))

    icons = str(files)

    icons = icons.replace('[', '')
    icons = icons.replace(']', '')
    icons = icons.replace("'", '')
    icons = icons.replace(", ", ' ')
    icons = 'none ' + icons

    # create a panel
    z = nuke.Panel('Labelizer...')

    z.addSingleLineInput('new label', oldLabel)
    z.addSingleLineInput('size', int(oldSize))

    if (selNode.Class()) == ('BackdropNode'):
        z.addSingleLineInput('order', int(oldOrder))

    if (selNode.Class()) == ('StickyNote'):
        z.addEnumerationPulldown('align', '<left> <center> <right>')

    z.addEnumerationPulldown('icon', icons)

    z.setWidth(800)
    result = z.show()

    # if user hits OK
    if result == True:

        newLabel = z.value('new label')
    
        try:
            newSize = int(z.value('size'))
        except:
            newSize = oldSize

        if selNode.Class() == ('BackdropNode'): # change Backdrop

            #selNode['label'].setValue('<center>' + newLabel)
            selNode['note_font_size'].setValue(float(newSize))

            newOrder = int(z.value('order'))
            selNode['z_order'].setValue(newOrder)

            icon = z.value('icon')
            insertIcon = ('<img src = "%s">' %(icon))

            if icon == 'none':
                selNode['label'].setValue('<center>' + newLabel)
            else:
                selNode['label'].setValue('<center>' + insertIcon + newLabel)


        elif selNode.Class() == ('StickyNote'): # change Sticky Note
            newAlign = z.value('align')

            #selNode['label'].setValue(newAlign + newLabel)
            selNode['note_font_size'].setValue(float(newSize))

            icon = z.value('icon')
            insertIcon = ('<img src = "%s">' %(icon))

            if icon == 'none':
                selNode['label'].setValue('<center>' + newLabel)
            else:
                selNode['label'].setValue('<center>' + insertIcon + newLabel)


        else: # change Dot
            #selNode['label'].setValue(newLabel)
            selNode['note_font_size'].setValue(float(newSize))

            icon = z.value('icon')
            insertIcon = ('<img src = "%s">' %(icon))

            if icon == 'none':
                selNode['label'].setValue('<center>' + newLabel)
            else:
                selNode['label'].setValue('<center>' + insertIcon + newLabel)


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
        
        allOperList = ['over', 'plus', 'screen', 'mask', 'multiply', 'overlay', 'from', 'difference', 'atop', 'average', 'color-burn', 'color-dodge', 'conjoint-over', 'copy',
                        'disjoint-over', 'divide', 'exclusion', 'geometric', 'hard-light', 'hypot', 'in', 'matte', 'max',
                        'min', 'minus', 'out', 'soft-light', 'stencil', 'under', 'xor']

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

        allOperList = ['union', 'in','stencil', 'minus', 'out', 'absminus', 'b-if-not-a', 'divide', 'from', 'max', 'min',  'multiply',  'plus', 'xor']

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

    z.setWidth(800)
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



if __name__ == '__main__':
    smartLabel()