"""this is executed when you press '.' in the ogre window, the viewer main window.
used for quick testing of py commands."""

import naali
naali = reload(naali) #hopefully allows devving naali.py without naali restarts
import rexviewer as r
import math

print "--- *** ---"

#print dir(r)

#some prim
idnum = 720011 #the cube most far away from the screen in Toni & Petri 's test sim
#idnum = 0
new_id = 9999999

#av ent
av_entid = 8880000

def rotate(e):
    p = e.placeable
    o = p.Orientation    
    #newort = (o.scalar(), o.x(), o.y() + 0.5, o.z())
    o.setY(o.y() + 0.5)
    print "Rotating to ort:", o
    p.Orientation = o
    #assert e.orientation[2] > (oldz+0.9) #xxx some logic fail here?
    #print "TEST ORIENTATION SUCCEEDED", e.orientation[2], oldortz
    
def move(e):
    p = e.placeable
    pos = p.Position
    #oldx = pos.x()
    #newpos = (p[0] - 1, p[1], p[2])
    pos.setX(pos.x() + 1) #change the x-coordinate
    print "Moving to move to pos:", pos
    p.Position = pos

if 0:
    print "Testing taking a screenshot..."
    
    path = "pymodules/webserver/screenshot/"
    pic = "current.png"
    
    hmm = r.takeScreenshot(path, pic)
    
if 0:
    print "Testing event sending, camera for now..."#   , r.SwitchCameraState
    hmm = r.sendEvent(r.SwitchCameraState)
    print "test done?", hmm

if 0:
    print "Testing camera swap..."
    hmm = r.switchCameraState()
    #print hmm
    
if 0: #get entity
    #idnum = new_id
    idnum = naali.getCamera().Id
    print "Getting entity id", idnum,
    e = naali.getEntity(idnum)
    print "got:", e
    #print dir(r)
    #rotate(e)
    #move(e)

if 0: #test avatartracking, works :)
    try:
        a = naali.getUserAvatar()
    except ValueError:
        print "could find the user avatar"
    else:
        print "<:::",
        print "Avatar pos:", a.placeable.Position,
        print ":::>"
        """
        perhaps some local script could track movement?
        make a sound of a nearby object of interest, 
        like when a pet or a friend moves?
        """
        
        if 0:
            #test what happens when we move the av
            #a.pos = a.pos[0] + 1, a.pos[1], a.pos[2]
            """crash, because of how network updates are coded in the internals: 
            XXX RexServerConnecion.cpp
            RexServerConnection::SendMultipleObjectUpdatePacket(std::vector<Scene::EntityPtr> entity_ptr_list)
            const Foundation::ComponentInterfacePtr &prim_component = entity_ptr_list[i]->GetComponent("EC_OpenSimPrim");
            (because avatars don't have the prim component"""
            
            #rotating the av
            rotate(a)

if 0: #push an event, input and/or chat
    #from eventsource import viewer
    #from modulemanager import m 
    import core.circuits_manager
    mm = core.circuits_manager.ComponentRunner.instance
    print mm
    
    #mm.INPUT_EVENT(r.MoveForwardPressed)
    
    #a chat message again now too
    #mm.RexNetMsgChatFromSimulator("Bob", "- that's me, Bob.")
    
    #previous pyglet stuff, was an ncoming chat msg event
    #m.dispatch_event('on_chat', "input", "testing")
    #print viewer._event_stack

if 0: #create entity
    print "Testing entity creation"
    meshname = "axes.mesh"
    
    avatar = naali.getUserAvatar()
    ent = naali.createMeshEntity(meshname)
    #print "New entity created:", ent, ent.placeable.Position
    ent.placeable.Position = avatar.placeable.Position

    #from PythonQt.QtGui import QVector3D as Vec
    #ent.placeable.Scale = Vec(0.1, 0.1, 0.1)
    #print "new pos", ent.pos, ent.scale

if 0: #placeable and text tests
    print "Testing..."
    e = r.getEntity(8880005)    

    #~ try:
        #~ e.pos = 1
    #~ except Exception, e:
        #~ print e
        
    #e.orientation = "well this ain't a quarternion."
    #e.scale = ("does", "this", "work")
    def test():
        print "this ain't a string..."
    
    e.text = "swoot"
    e.text = 1
    e.text = ("swoot", "ness")
    e.text = (1, 2)
    e.text = test
    
    e.pos = 1
    
    print e.text, e.pos, e.scale, e.orientation
    
if 0: #send chat
    r.sendChat("hello from new realXtend Naali!")
    #print "called sendchat ok"
    
if 0: #print test
    r.logInfo("this is a test print!")
    
if 0: #camera entity - it is an entity nowadays, and there is EC cam even
    try:
        cament = naali.getCamera()
        print "CAM:", cament.Id
    except ValueError:
        print "no CAM"
    else:
        p = cament.placeable
        print p.Position, p.Orientation

        import PythonQt.QtGui
        from PythonQt.QtGui import QQuaternion as Quat
        from PythonQt.QtGui import QVector3D as Vec
        ort = p.Orientation
        rot = Quat.fromAxisAndAngle(Vec(0, 1, 0), 10)
        #ort *= Quat(0, -.707, 0, .707)
        ort *= rot
        p.Orientation = ort
        
        #ec cam stuff:
        print "FOV:", cament.camera.GetVerticalFov()
        
        

if 0: #calcing the camera angle around up axis for web ui
    import PythonQt.QtGui
    from PythonQt.QtGui import QQuaternion
    from PythonQt.QtGui import QVector3D
    import mathutils as mu

    def toAngleAxis(quat): 
        #no worky, so resorted to euler conversion
        import PythonQt
        import math

        lensq = quat.lengthSquared()
        ang = 2.0 * math.acos(quat.scalar())

        invlen = lensq ** 0.5
        vec = PythonQt.QtGui.QVector3D(quat.x() * invlen,
                                       quat.y() * invlen,
                                       quat.z() * invlen)

        return vec, ang

    cament = naali.getCamera()
    p = cament.placeable

    #print toAngleAxis(p.Orientation)

    ort = p.Orientation
    euler = mu.quat_to_euler(ort)
    #print euler
    start = QQuaternion(0, 0, -0.707, -0.707)
    #print start
    rot = QQuaternion.fromAxisAndAngle(QVector3D(0, 1, 0), -10)
    new = start * rot
    print ort
    print new
    #p.Orientation = new
    #print mu.euler_to_quat(euler), ort
        
if 0: #avatar set yaw (turn)
    #a = -1.0
    a = 0
    print "setting avatar yaw with %f" % a
    r.setAvatarYaw(a)

if 0: #avatar rotation #XXX crashes when the avatar is not there! XXX
    x = 0
    y = 0 
    z = 0.1 #this is the actual rotation thingie
    w = 0
    print "rotating the avatar to", (x, y, z, w)    
    r.setAvatarRotation(x, y, z, w)
    
if 0: #create a new qt canvas
    try:
        c = r.c
    except: #initial run
        c = r.createCanvas()
        r.c = c
    else: #the canvas has already been created
        #import PythonQt
        #print globals()
        #print '=============='
        #print 'box' in globals()
        #print dir(PythonQt)
        #print box
        print "~~~"
        #print "test t:", test
        #print "canvas t:", __canvas__
    print c
    
if 0: #add a signal handler to the ui loaded above, i.e. create a slot and connect it
    r.c.label.text = "py-commanded"
    def changed(v):
        print "val changed to: %f" % v
    #print r.c.label.connect('clicked()', changed)
    print r.c.doubleSpinBox.connect('valueChanged(double)', changed)
    print r.c.children()
    print dir(r.c)
    
if 0: #for the box test ui created in code - works
    # define our own python method that appends the text from the line edit
    # to the text browser
    box = r.c
    def appendLine():
        box.browser.append(box.edit.text)
    box.button1.connect('clicked()', appendLine)
    box.edit.connect('returnPressed()', appendLine)

if 0: #sys.path PYTHONHOME etc fix attempts
    import os
    print os.getenv("PYTHONHOME")
    
    import sys
    print sys.path
    
    import modulemanager
    print modulemanager.__file__
    
if 0: #python-ogre test - using the extension lib in the embedded context :o
    #import sys
    #sys.path.append('pymodules/ogre.zip')
    #didn't work for some reason yet - should .pyd s work from zips too?
    #apparently it should work: http://mail.python.org/pipermail/python-list/2008-March/653795.html
    
    #based on the info in http://www.ogre3d.org/addonforums/viewtopic.php?f=3&t=8743&hilit=embed
    import ogre.renderer.OGRE as ogre
    root = ogre.Root.getSingleton()
    #print dir(r)
    print root.isInitialised()
    rs = root.getRenderSystem()
    #rs.setAmbientLight(1, 1, 1)
    vp = rs._getViewport()
    #print vp
    bg = vp.getBackgroundColour()
    #only affects when not connected, when caelum is not there i figure
    vp.setBackgroundColour(ogre.ColourValue(0.1, 0.2, 0))
    
    cam = vp.getCamera()
    #print cam
    
    sm = root.getSceneManager("SceneManager")
    print sm
    
    def drawline():
        try:
            mcounter = r.mcounter
        except: #first execution
            print "first exec"
            mcounter = 1
        else:
            mcounter += 1
            #print "incremented manual object counter to", mcounter
        r.mcounter = mcounter
        print "Creating manual object index", mcounter
        mob =  sm.createManualObject("manual%d" % mcounter)
        mnode = sm.getRootSceneNode().createChildSceneNode("manual%d_node" % mcounter)
        
        try:
            mmaterial = r.mmaterial
        except: #first execution
            mmaterial = ogre.MaterialManager.getSingleton().create("manual1Material","debugger")
            mmaterial.setReceiveShadows(False)
            tech = mmaterial.getTechnique(0)
            tech.setLightingEnabled(True)
            pass0 = tech.getPass(0)
            pass0.setDiffuse(0, 0, 1, 0)
            pass0.setAmbient(0, 0, 1)
            pass0.setSelfIllumination(0, 0, 1)
            r.mmaterial = mmaterial
            print "created the manual material"
        else:
            pass
            #print "got the existing manual material"
            
        mob.begin("manual1Material", ogre.RenderOperation.OT_LINE_LIST)
        mob.position(40, 240, 55 - mcounter)
        mob.position(240, 10, 10 + mcounter)
        #etc 
        mob.end()
        mnode.attachObject(mob)
        
    drawline()

if 0: #pydoc can hopefully serve / give us api docs of pythonqt somehow
    import sys
    import PythonQt
    sys.argv = ['PythonQt']
    import pydoc
    pydoc.gui()

if 0: #pythonqt introspec
    #print "Importing PythonQt..."
    import PythonQt
    import PythonQt.QtCore

    #k = PythonQt.QtCore.Qt.AltModifier
    #print k, type(k), dir(k)
    #print dir(PythonQt.Qt)
    #qapp = PythonQt.Qt.QApplication.instance()
    #print qapp.changeOverrideCursor

    #import PythonQt.QtGui as gui
    #print dir(gui)
    #cursor = gui.QCursor()
    #print cursor, cursor.shape()
    #cursor.setShape(1)
    #qapp.setOverrideCursor(cursor)

    #print PythonQt.QtCore.Qt.Vertical
    #print "Importing PythonQt.QtGui..."

    #import PythonQt.QtUiTools as uitools
    #print dir(uitools.QUiLoader)
    #print dir(gui.QTreeWidgetItem)

    #UiWidgetProperties = PythonQt.__dict__['UiServices::UiWidgetProperties']
    #print type(UiWidgetProperties), dir(UiWidgetProperties)
    #print UiWidgetProperties.WidgetType #the enum should be moved to be inside the class XXX

if 0: # EC_OgreCamera
    import naali
    cam = naali.getCamera()
    if cam is not None:
        print dir(cam), cam.className, cam

    #the slot is there now also directly, not with the 'pythonified' name
    #print "cam from slot directly:", naali.GetCameraEntity()
    from __main__ import _naali
    print dir(_naali)
    _naali.delete()
    _naali.deleteLater()

if 0:
    import naali
    def keypressed(e):
        print e
    #print dir(naali.inputcontext)
    #naali.inputcontext.disconnect()
    naali.inputcontext.connect('OnKeyEvent(KeyEvent&)', keypressed)

if 0: #QVector3D
    import PythonQt.QtGui
    #print dir(PythonQt.QtGui)
    v3 = PythonQt.QtGui.QVector3D()
    print v3
    print dir(v3)
    v3.setX(1)
    print v3.x()

    pointa = PythonQt.QtGui.QVector3D(0,0,0)
    pointb = PythonQt.QtGui.QVector3D(2, 2, 0)
    direction = PythonQt.QtGui.QVector3D(1, 1, 0)
    print pointa.distanceToLine(pointb, direction)
    
if 0: #QQuaterinion
    import PythonQt.QtGui
    q1 = PythonQt.QtGui.QQuaternion(1, 0, 0, 1)
    q2 = PythonQt.QtGui.QQuaternion(0.707, 0, 0.707, 0)
    print q1, q2
    
    q3 = q1*q2
    q1 *= q2
    print q3, q1

if 0:
    import PythonQt.QtCore
    
    point_a_tl = PythonQt.QtCore.QPoint(2,2)
    point_a_br = PythonQt.QtCore.QPoint(5,5)
    
    point_b_tl = PythonQt.QtCore.QPoint(3,3)
    point_b_br = PythonQt.QtCore.QPoint(7,7)
    
    rect_a = PythonQt.QtCore.QRect(point_a_tl, point_a_br)
    print "Rect A: ", rect_a.toString()
    rect_b = PythonQt.QtCore.QRect(point_b_tl, point_b_br)
    print "Rect B: ", rect_b.toString()
    print "intersects: ", rect_a.intersects(rect_b)
    
    rect_c = rect_a.intersected(rect_b)
    print "intersected:", rect_c.toString()

if 0:
    from PythonQt.QtGui import *

    group = QGroupBox()
    box = QVBoxLayout(group)
    print dir(box)
    push1 =  QPushButton(group)
    box.addWidget(push1)
    push2 =  QPushButton(group)
    box.addWidget(push2)
    check =  QCheckBox(group)
    check.text = 'check me'
    group.title = 'my title'
    push1.text = 'press me'
    push2.text = 'press me2'
    box.addWidget(check)
    group.show()

if 0:
    box = r.c.widget
    def funk(item):
        print "got index...", item
        box.treeWidget.currentItem().setText(0, "doooood")
    r.c.widget.treeWidget.disconnect('activated(QModelIndex)', r.c.itemActivated)
    r.c.itemActivated = funk
    r.c.widget.treeWidget.connect('activated(QModelIndex)', funk)
    print type(r.c)

if 0:
    box = r.c.widget.treeWidget
    box.clear()
    
if 0: #populating the EditGui window
    from PythonQt.QtGui import *
    from PythonQt.QtCore import QPoint
    box = r.c.widget
    box.label.text = "hmm"

    children = []
    children.append(QTreeWidgetItem(box.treeWidget))
    children[0].setText(0, "swoot")
    children.append(QTreeWidgetItem(box.treeWidget))
    children.append(QTreeWidgetItem(box.treeWidget))
    children.append(QTreeWidgetItem(box.treeWidget))
    print len(children)
    #~ def test(item, idx):
        #~ print "worked...", item, idx
    #~ box.treeWidget.connect('itemActivated(QTreeWidgetItem)', test)
    #box.treeWidget.connect('itemActivated', test)
    #box.treeWidget.itemClicked.connect(box.treeWidget.itemClickedSetSelected)
    
    #~ pos = QPoint(0,1)
    #~ thingie5 = box.treeWidget.indexAt(pos)  
    #print box.treeWidget.findChild
    #index = box.treeWidget.currentIndex()
    #print box.treeWidget.activated(index), index
    #print dir(box.treeWidget)

if 0:
    box = r.c.widget
    #print box, dir(box.treeWidget)
    text = box.treeWidget.currentItem().text(0)
    print text
    print type(text), r.c.widgetList
    print r.c.widgetList[720010]

if 0: #QtUI::UICanvas::External ?! not here...
    from PythonQt.QtUiTools import QUiLoader
    from PythonQt.QtCore import QFile, QIODevice
    #print dir(quil)  
    #print dir(PythonQt.QtCore.QIODevice)
    loader = QUiLoader()
    canvas = r.createCanvas(0)
    
    file = QFile("pymodules/usr/editobject.ui")
    iodev = QIODevice(file)

    widget = loader.load(file)
    canvas.AddWidget(widget)
    canvas.Show()
    
if 0: #collada load testing
    import collada
    print collada.Collada
    try:
        pycollada_test
    except:
        import pycollada_test
    else:
        pycollada_test = reload(pycollada_test)

if 0: #canvas size edit
    box = r.c
    #print dir(box.widget.size)
    #print box.widget.size.width()#, box.widget.size.height
    #print type(box.canvas)
    #box.canvas.size.setHeight(600)#
    #box.canvas.adjustSize()
    width = box.widget.size.width()
    height = box.widget.size.height()
    print width, height
    box.canvas.resize(width, height)
    #print box.canvas.resize(380, 250)
    
if 0: #ogre cam test and vectors
    import ogre.renderer.OGRE as ogre
    root = ogre.Root.getSingleton()
    #print dir(r)
    print root.isInitialised()
    rs = root.getRenderSystem()
    
    vp = rs._getViewport()
    
    
    #~ print dir(ogre.Vector3)
    #~ vec = ogre.Vector3(5, 5, 5).normalisedCopy() 
    #~ print vec, type(vec)
    cam = vp.getCamera()
    
    #print dir(cam)
    #print cam.Orientation, cam.DerivedOrientation, cam.getOrientation()
    #~ print "\n"
    #~ print cam.getRight(), cam.getUp()

if 0:
    canvas = r.c.canvas
    for child in canvas.children():
        child.delete()
    canvas.close()
    #canvas.deleteLater()
    
if 0: #pygame window test
    try:
        r.pygame
    except AttributeError: #first run
        import pygame
        r.pygame = pygame
        s = pygame.display.set_mode((320, 200))
        print s,
        r.pygame_s =  s #screen
        print r.pygame_s
        
    else:
        s = r.pygame_s
    print s
    
    s.fill((64, 95, 73))
    pygame.display.flip()
    
    #works :)=======

if 0: #testing the removal of canvases
    canvas = r.c.canvas
    modu = r.getQtModule()
    #print dir(modu)
    bool = modu.RemoveCanvasFromControlBar(canvas)
    print bool
    
if 0: #getUserAvatar 
    ent = naali.getUserAvatar()
    print "User's avatar_id:", ent.Id
    #print "Avatar's mesh_name:", ent.mesh.GetMeshName(0)
    #ent.mesh = "cruncah1.mesh"
    
if 0: #test changing the mesh asset a prim is using
    ent_id = 2088826433
    #print arkku_id, type(arkku_id)
    ent = naali.getEntity(ent_id)
    print "Test entity:", ent
    print ent.mesh
    #ent.mesh = 1 #should raise an exception
    #ruukku = "681b1680-fab5-4203-83a7-c567571c6acf"
    #penkki = "04d335b6-8f0c-480e-a941-33517bf438d8"
    jack = "6b9cf239-d1ec-4290-8bc7-f5ac51288dea" #on w.r.o:9000
    ent.mesh.SetMesh(jack) #"35da6174-8743-4026-a83e-18b23984120d"
    print "new mesh set:", ent.mesh
    
    print "sending prim data update to server"
    r.sendRexPrimData(ent.Id) #arkku
    print "..done", ent.mesh
    
if 0: #property editor tests
    #print r.c
    #print r, dir(r)
    pe = r.getPropertyEditor()
    #print pe, pe.setObject, pe.show
    pe.setObject(r.c.widget)
    pe.show()
    
if 0: #getting args from outside to run tests automatically
    import os
    naaliargs = os.getenv('NAALIARGS')
    print naaliargs

if 0:
    #print r.c.widget.move_button, dir(r.c.widget.move_button)
    #r.c.canvas.Show()
    print r.c.widget.move_button.isChecked(), r.c.widget.rotate_button.isChecked(), r.c.widget.scale_button.isChecked()
    #print  dir(r.c.widget.move_button)
    r.c.widget.move_button.setChecked(False)
    
if 0: #camera FOV
    #fov = r.getCameraFOV()
    #rightvec = V3(r.getCameraRight())
    fov = naali.getCamera().camera.GetVerticalFov()
    print "FOV:", fov
    campos = naali.getCamera().placeable.Position
    #ent = naali.getUserAvatar()
    #entpos = V3(ent.pos)
    #width, height = r.getScreenSize()
    import naali
    rend = naali.renderer
    #print r.getScreenSize()
    print rend.GetWindowWidth(), rend.GetWindowHeight()

    if 0: #didn't port the above vec getters now to current
        x = 613
        y = 345
        normalized_width = 1/width
        normalized_height = 1/height
    
        #print x * normalized_width
    
        length = (campos-entpos).length
        worldwidth = (math.tan(fov/2)*length) * 2

        #print campos, entpos, length, fov, width, height
    
        ent1 = r.createEntity("cruncah.mesh")
        ent1.pos = pos.x, pos.y+worldwidth/2, pos.z
        ent2 = r.createEntity("cruncah.mesh")
        ent2.pos = pos.x, pos.y+worldwidth/2, pos.z
        #~ newpos = 
        #~ print newpos
    
    
if 0: #bounding box tests. not ported to naali.Entity now, is not used anymore by obedit either?
    #robo 1749872183
    #ogrehead 1749872798
    ent = r.getEntity(1749871222)#naali.getUserAvatar()
    from editgui.vector3 import Vector3 as V3
    #~ print ent.boundingbox
    bb = list(ent.boundingbox)
    print bb
    #~ scale = list(ent.scale)
    #~ min = V3(bb[0], bb[1], bb[2])
    #~ max = V3(bb[3], bb[4], bb[5])
    #~ height = abs(bb[4] - bb[1]) + scale[0]#*1.2
    #~ width = abs(bb[3] - bb[0]) + scale[1] #*1.2
    #~ depth = abs(bb[5] - bb[2]) + scale[2]#*1.2
    #~ #print ent.pos, 
    #~ print min, max, height, width, depth
    
    #~ r.box = r.createEntity("Selection.mesh")
    #~ r.box.pos = ent.pos
    
    #~ r.box.scale = height, width, depth#depth, width, height
    #~ r.box.orientation = ent.orientation
    
    
    #~ min_ent = r.createEntity("cruncah1.mesh")
    #~ min_ent.scale = 0.3, 0.3, 0.3
    #~ min_ent.pos = pos[0] + min.x, pos[1] + min.y, pos[2] + min.z 
    
    #~ max_ent = r.createEntity("cruncah1.mesh")
    #~ max_ent.scale = 0.3, 0.3, 0.3
    #~ max_ent.pos = pos[0] + max.x, pos[1] + max.y, pos[2] + max.z
    
if 0: #login - for running tests automatically
    print "starting opensim login"
    #user, pwd, server = "Test User", "test", "localhost:9000"
    user, pwd, server = "d d", "d", "world.evocativi.com:8002"
    r.startLoginOpensim(user, pwd, server)
    
if 0: #getserverconnection test
    #print dir(r)
    #print "YO", r.getTrashFolderId()
    #r.deleteObject(2351241440)
    worldstream = r.getServerConnection()
    
    #print worldstream, dir(worldstream), worldstream.SendObjectDeRezPacket
    worldstream.SendObjectDeRezPacket(2891301779, r.getTrashFolderId())
    #ent = r.getEntity(r.getUserAvatarId())
    #worldstream.SendObjectDeletePacket(1278500474, True)
    #~ ent = r.getEntity(2208825114)
    #~ print ent

if 0: #getrexlogic test
    l = r.getRexLogic()
    print l, dir(l)
    #class entity_id_t(int): pass
    #entid = entity_id_t(2)
    #l.SendRexPrimData(entid)
    
if 0: #rexlogic as service with qt mechanism
    #from __main__ import _naali
    #l = _naali.GetWorldLogic()
    #print l, dir(l)
    import naali
    qent = naali.worldlogic.GetUserAvatarEntityRaw()
    if qent is not None:
        print qent.Id
        pyent = r.getEntity(qent.Id)
        print pyent, pyent.id
        
if 0: #using entity directly to get components, without PyEntity
    import naali
    qent = naali.worldlogic.GetUserAvatarEntityRaw()
    if qent is not None:
        print qent.Id
        print dir(qent)
        p = qent.GetComponentRaw("EC_Placeable")
        print p, p.Position
        
        #ent = naali.Entity(qent)
        #print ent, ent.placeable, ent.placeable.Position
        
        ent = naali.getEntity(qent.Id)
        print ent, ent.placeable, ent.placeable.Position
    
if 0: #undo tests
    e = r.getEntity(1752805599)
    print e.prim, e.uuid
    e_uuid = "d81432f2-28f3-4e05-ac8a-abb4b625dbe4-"
    worldstream = r.getServerConnection()
    #print worldstream, dir(worldstream), worldstream.SendObjectDeRezPacket
    worldstream.SendObjectUndoPacket(e.uuid)
    
if 0: #undo tests and ent.uuid
    e = naali.getEntity(1752805599)
    print e, e.prim.FullId
    worldstream = r.getServerConnection()
    #print worldstream, dir(worldstream), worldstream.SendObjectDeRezPacket
    worldstream.SendObjectSelectPacket(ent.id)
    
if 0: #updateflag checks, duplicate tests
    e = naali.getEntity(2054915991)
    print e, e.prim.FullId, e.prim.UpdateFlags
    ws = r.getServerConnection()
    #print dir(ws)
    #x, y, z = e.placeable.Position.x(), ... #didn't port this unused line to new version
    ws.SendObjectDuplicatePacket(e.Id, e.prim.UpdateFlags, 1, 1, 1)
    
if 0: #proxywidget signal connecting
    #~ from PythonQt.QtUiTools import QUiLoader
    #~ from PythonQt.QtCore import QFile
    #~ #prop = r.getUiWidgetProperty()
    #~ #print prop, dir(prop), prop.widget_name_
    #~ loader = QUiLoader()
    #~ uifile = QFile("pymodules/editgui/editobject.ui")
    #~ ui = loader.load(uifile)
    #~ uiprops = r.createUiWidgetProperty()
    #~ uiprops.widget_name_ = "WOOT"
    #~ widget = r.createUiProxyWidget(ui, uiprops)
    #~ print widget, dir(widget)
    
    #~ uism = r.getUiSceneManager()
    #~ if uism.AddProxyWidget(widget):
        #~ print "WORKED!"
    
    #~ modu =  r.getQtModule()
    #~ print modu, dir(modu)
    #~ whee = modu.whee()
    #~ print whee, dir(whee)#, whee.about()
    
    print r.c, r.c.proxywidget, dir(r.c.proxywidget)
    def whee(boo):
        print boo
    r.c.proxywidget.connect('Visible(bool)', whee)

if 0: #get entity by (prim) uuid
    #uuid = "cac0a9bf-2ee3-427a-bf2b-5a2f17cb3155"
    e = r.getEntityByUUID(uuid)
    print e, "by uuid", uuid

if 0: #search where a given texture is used
    #uuid = "cac0a9bf-2ee3-427a-bf2b-5a2f17cb3155" #antont local fishworld screen
    #uuid = "3edf2f27-411e-4a80-af8d-a422c014532e" #prim school project test display
    uuid = 'a07893e6-3631-4ee0-b9a4-1a4e07eed5be' #mesh
    #print applyUICanvasToSubmeshesWithTexture(canvas, uuid)
    
if 0:
    #print r.c, dir(r.c)
    print r.manager
    print dir(r.manager)
    
    channels = r.manager.channels
    #print channels
    for item in channels:
        for handler in r.manager._getHandlers(item):
            print handler.channels#dir(handler)
            
if 0:
    import PythonQt
    from PythonQt.QtGui import QTreeWidgetItem, QInputDialog, QLineEdit
    box = r.c.widget.findChild("QVBoxLayout")
    print box, dir(box), box.name
    line = QLineEdit()
    box.addWidget(line)

if 0: #a c++ side test func for api dev
    ret = r.randomTest()
    print ret
    print ret.map, ret.about(), ret.uuid, ret.list()
    l = ret.list()
    print dir(l)
    print l.count(2)
    for i in l:
        print i
    #print qm, dir(qm)
    #~ print r.c.widget, r.c.proxywidget
    #~ pe = r.getPropertyEditor()
    #~ #print pe, pe.setObject, pe.show
    #~ pe.setObject(r.c.proxywidget)
    #~ pe.show()

if 0: #QRenderer
    #rend = r.getQRenderer()
    #print rend
    #print rend.FrustumQuery
    #print dir(rend)
    #print rend.

    #import PythonQt
    #import __main__
    #print dir(__main__)
    #from __main__ import _naali
    #print dir(PythonQt)
    #PythonQt.__main__
    #print _naali.GetRenderer()

    import naali
    print naali.renderer

    r = naali.renderer
    r.HideCurrentWorldView()
    r.Render()
    import time; time.sleep(1)
    r.ShowCurrentWorldView()

if 0: #worldstream
    worldstream = r.getServerConnection()
    print "send drop bomb:", worldstream.SendGenericMessage("DropBomb", ["here", "soon", "BIG"])

if 0: #scene, aka. SceneManager
    import naali
    s = naali.getScene("World")
    print s

if 0: #javascript service
    import naali
    from naali import runjs
    cam = naali.getCamera()
    runjs('print("Hello from JS! " + x)', {'x': naali.renderer})
    runjs('print("Another hello from JS! " + x)', {'x': naali.inputcontext})
    runjs('print("Some camera! " + x)', {'x': cam.camera})
    #py objects are not qobjects. runjs('print("Some camera, using naali :O ! " + x.getCamera())', {'x': naali})
    runjs('print("Camera Entity " + x)', {'x': cam.qent})
    runjs('print("Camera placeable pos: " + pos)', {'pos': cam.placeable.Position})
    #not exposed yet. runjs('print("QVector3D: " + new QVector3D())', {})
    #runjs('var a = {"a": true, "b": 2};')
    #runjs('print(a.a + ", " + a.b)')
    #runjs('print(JSON.stringify(a))')
    #runjs('print("1 + 1 == " + 1 + 1)')
    #runjs('print("1 - 1 == " + 1 - 1)')
    print ", done."

    if 0:
        runjs('var b = new QPushButton;')
        runjs('b.text = "hep";')
        runjs('b.show();')

if 0: 
    print r.c, dir(r.c)
    print r.c.widget
    print dir(r.c.proxywidget)
    r.c.proxywidget.hide()
    
if 0: #qprim
    #qprim = r.getQPrim(1680221423)
    e = naali.getEntity(1680221423)
    qprim = e.prim
    mats = qprim.Materials
    print mats
    
    #~ qprim.Materials = mats
    
    #~ edited_mats = mats
    
    #~ keys = {}
    #~ id = 0
    for key in mats.itervalues():
        if key[1] == "":
            print "swoot"
        #~ id += 1
    
    #~ #print keys, mats.keys(), mats[keys[0]]

if 0: #qplaceable
    id = 2138143966
    #qplace = r.getQPlaceable(id)
    e = naali.getEntity(id)
    qplace = e.placeable
    print qplace, qplace.Position

    oldz = qplace.Position.z()
    print oldz, "==>",

    import PythonQt.QtGui
    from PythonQt.QtGui import QVector3D
    change_v = QVector3D(0, 0, 0.1)
    #dir shows __add__ but for some reason doesn't work out of the box :(
    #"unsupported operand type(s) for +=: 'QVector3D' and 'QVector3D'"
    #qplace.Position += change_v
    #qplace.Position + change_v

    #bleh and this changes the val in the vec, but doesn't trigger the *vec* setter, 
    #so no actual change in Naali internals
    #qplace.Position.setZ(oldz + 0.1)
  
    newpos = qplace.Position
    newpos.setZ(oldz + 0.1)
    qplace.Position = newpos
    print qplace.Position.z(), "."    
        
if 0:
    from PythonQt.QtCore import QFile, QSize
    from PythonQt.QtGui import QLineEdit, QHBoxLayout,  QLabel, QPushButton, QSizePolicy, QIcon
    
    box = r.c.widget.findChild("QHBoxLayout", "meshLine")
    #print box.layoutSpacing
    button = QPushButton()

    icon = QIcon("pymodules/editgui/ok.png")
    icon.actualSize(QSize(16, 16))
    
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    button.setMaximumSize(QSize(16, 16))
    button.setMinimumSize(QSize(16, 16))

    button.text = ""
    button.name = "Apply"
    button.setIcon(icon)
    box.addWidget(button)
    
    #~ line = r.c.widget.findChild("QLineEdit", "meshLineEdit")
    #~ print line.sizePolicy.horizontalPolicy(), QSizePolicy.Expanding
    
if 0:
    print "Test"
    PRIMTYPES = {
        "0": "Texture", 
        "45": "Material"
    }
    
    def swoot():
        print "booyah!"
    
    def noswoot():
        print "!booyah!"
        
    from PythonQt.QtUiTools import QUiLoader
    from PythonQt.QtCore import QFile, QSize
    from PythonQt.QtGui import QLineEdit, QHBoxLayout, QComboBox, QLabel
    
    loader = QUiLoader()
    uifile = QFile("pymodules/editgui/materials.ui")
    ui = loader.load(uifile)
    uism = naali.ui
    uiprops = r.createUiWidgetProperty() #note: createUiWidgetProperty doesn't exist anymore -Stinkfist
    uiprops.show_at_toolbar_ = False
    uiprops.widget_name_ = "Test"
    uiprops.my_size_ = QSize(ui.size.width(), ui.size.height())
    pw = r.createUiProxyWidget(ui, uiprops)
    uism.AddProxyWidget(pw)
    r.formwidget = ui.gridLayoutWidget
    r.pw = pw
    r.pw.show()
    
    #print dir(r.formwidget), r.formwidget.rowCount()

    #~ qprim = r.getQPrim(2985471908)
    #~ mats = qprim.Materials
    #~ print mats#, r.formwidget.formLayout.children() 
    #qprim.Materials = mats
    #~ r.elements = []
    #~ indx = 1
    #~ for tuple in mats.itervalues():
        
        #~ print tuple, tuple[0] == "45"
        #combo = QComboBox()
        #combo.addItem("Material")
        #combo.addItem("Texture")
        #~ line = QLineEdit()
        #~ line.text = tuple[1]
        #~ line.name = "lineEdit_"+str(indx)
        #~ indx += 1
        #~ label = QLabel()
        #~ label.name = PRIMTYPES[tuple[0]]#tuple[0]
        #~ label.text = PRIMTYPES[tuple[0]]
        #~ r.elements.append((label, line))
        #~ r.formwidget.formLayout.addRow(label, line)
    
    #print r.elements
    #~ #print dir(r.formwidget)
    #~ stuff =  r.formwidget.children()
    #~ for thingie in stuff:
        #~ print thingie.name#, thingie.name == "formLayout"
        #~ if thingie.name != "formLayout":
            #~ thingie.delete()


    #~ r.pw.show()

if 0:
    box = r.formwidget.findChild("QGridLayout", "gridLayout")
    print box.rowCount()
    
if 0:
    from PythonQt.QtCore import QFile, QSize
    from PythonQt.QtGui import QLineEdit, QHBoxLayout, QComboBox, QLabel, QPushButton, QSizePolicy, QIcon
    
    box = r.formwidget.findChild("QGridLayout", "gridLayout")
    #print box.rowCount()

    label = QLabel()
    label.text = "n/a"
    
    row = 3
    
    box.addWidget(label, row, 0)
    #print r.c.materialDialogFormWidget
    line = QLineEdit()#QLineEdit()
    line.text = "whee"
    line.name = "whee"
    
    box.addWidget(line, row, 1)


    button = QPushButton()
    icon = QIcon("pymodules/editgui/ok.png")
    icon.actualSize(QSize(16, 16))
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    button.setMaximumSize(QSize(16, 16))
    button.setMinimumSize(QSize(16, 16))
    button.text = ""
    button.name = "Apply"
    button.setIcon(icon)
    
    box.addWidget(button, row, 2)
    
    
    button = QPushButton()
    icon = QIcon("pymodules/editgui/cancel.png")
    icon.actualSize(QSize(16, 16))
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    button.setMaximumSize(QSize(16, 16))
    button.setMinimumSize(QSize(16, 16))
    button.text = ""
    button.name = "Cancel"
    button.setIcon(icon)
    
    box.addWidget(button, row, 3)

if 0:
    from PythonQt.QtUiTools import QUiLoader
    from PythonQt.QtCore import QFile, QSize
    from PythonQt.QtGui import QLineEdit, QHBoxLayout, QComboBox, QLabel, QPushButton, QSizePolicy, QIcon
    loader = QUiLoader()
    uism = naali.ui
    
    #~ uifile3 = QFile("pymodules/editgui/tab.ui")
    #~ ui3 = loader.load(uifile3)
    #~ uiprops3 = r.createUiWidgetProperty()
    #~ uiprops3.show_at_toolbar_ = False
    #~ uiprops3.widget_name_ = "tab"
    #~ uiprops3.my_size_ = QSize(ui3.size.width(), ui3.size.height())
    #~ pw3 = r.createUiProxyWidget(ui3, uiprops3)
    #~ r.pw3 = pw3
    #~ r.tab_manager = ui3.tabWidget
    #~ uism.AddProxyWidget(pw3)
    #~ r.pw3.show()

    uifile = QFile("pymodules/editgui/materials.ui")
    ui = loader.load(uifile)
    uiprops = r.createUiWidgetProperty()
    uiprops.show_at_toolbar_ = False
    uiprops.widget_name_ = "Test"
    uiprops.my_size_ = QSize(ui.size.width(), ui.size.height())
    pw = r.createUiProxyWidget(ui, uiprops)
    r.pw = pw    
    
    uifile2 = QFile("pymodules/editgui/editobject.ui")
    ui2 = loader.load(uifile2)
    uiprops2 = r.createUiWidgetProperty()
    uiprops2.show_at_toolbar_ = False
    uiprops2.widget_name_ = "editobject"
    uiprops2.my_size_ = QSize(ui2.size.width(), ui2.size.height())
    pw2 = r.createUiProxyWidget(ui2, uiprops2)
    r.pw2 = pw2

    r.tab_manager.addTab(r.pw, QIcon("pymodules/editgui/cancel.png"), "test")
    r.tab_manager.addTab(r.pw2,  QIcon("pymodules/editgui/cancel.png"),  "editobject")
    
if 0:
    from PythonQt.QtGui import QLineEdit, QHBoxLayout
    box =  r.c.materialDialogFormWidget.formLayout
    hor = QHBoxLayout()
    line = QLineEdit()
    hor.addWidget(line)
    print hor

if 0:
    from PythonQt.QtGui import QLineEdit, QHBoxLayout, QComboBox, QLabel
    combo = QComboBox()
    combo.addItem("aaaa")
    combo.addItem("bbbb")
    combo.addItem("cccc")
    combo.addItem("dddd")
    
    print combo.currentIndex, combo.findText("ccCc")

if 0:
    print r.c.propedit
    #~ r.c.propedit.setObject(r.c.propedit)
    #~ r.c.propedit.show()
    #~ props = r.createUiWidgetProperty()
    #~ props.show_at_toolbar_ = False
    #~ props.widget_name_ = "property editor"
    #~ r.test = r.createUiProxyWidget(r.c.propedit, props)
    #~ r.test.show()
    uism = naali.ui
    uism.AddProxyWidget(r.test)
    print r.test
    r.test.show()


if 0:
    import PythonQt
    from PythonQt.QtUiTools import QUiLoader
    from PythonQt.QtCore import QFile, QSize
    from PythonQt.QtGui import QLineEdit, QHBoxLayout, QComboBox, QLabel, QPushButton, QSizePolicy, QIcon, QWidget
    loader = QUiLoader()
    uifile = QFile("pymodules/objectedit/selection.ui")
    ui = loader.load(uifile)
    uism = r.getUiSceneManager()
    uiprops = r.createUiWidgetProperty(2) #note: createUiWidgetProperty doesn't exist anymore -Stinkfist
    uiprops.widget_name_ = "Thingie Rect"
    
    #uiprops.my_size_ = QSize(width, height) #not needed anymore, uimodule reads it
    proxy = r.createUiProxyWidget(ui, uiprops)
    uism.AddProxyWidget(proxy)
    proxy.setWindowFlags(0)
    
    ui.show()
    
    r.c.ui = ui
    print r.c.ui.geometry
    #~ r.c.ui.setGeometry(10, 60, 400, 400)
    
    #~ r.c.ui.hide()
    #~ r.c.ui = None
    
    #~ print r.c.ui
    #~ r.c.ui.setGeometry

    
if 0:
    for ent in r.c.sels:
        print ent.id
    worldstream = r.getServerConnection()
    print dir(worldstream)
    id1 = 1250116908
    id2 = 1250116909
    ids = [id1, id2]
    worldstream.SendObjectLinkPacket(ids)
    #~ worldstream.SendObjectDelinkPacket(ids)

if 0: #position as a qvec3d prop of placeable component
    import PythonQt.QtGui
    id = 2703563778
    ent = naali.getEntity(id)
    changevec = PythonQt.QtGui.QVector3D(0, 0, 1)
    print ent.placeable.Position, ent.placeable.Orientation, changevec
    ent.placeable.Position = ent.placeable.Position + changevec
    
    print ent.placeable.Position, ent.placeable.Orientation, changevec
    r.networkUpdate(id)

if 0:
    import PythonQt.QtGui
    a = PythonQt.QtGui.QVector3D(5, 5, 1)
    b = PythonQt.QtGui.QVector3D(5, 5, 0)
    print a == b, a.toString(), b.toString()
    

if 0: #sound add&remove
    e = naali.getUserAvatar()
    try:
        e.sound
    except AttributeError:
        print e.GetOrCreateComponentRaw("EC_AttachedSound")
        print "HAS SOUND COMPONENT:", e.HasComponent("EC_AttachedSound")
        #print naali.createComponent(e, "EC_AttachedSound") #temp workaround XXX
        print "created a new Sound component"

    s = e.sound
    print type(s), s

    #e.removeSound(s)
    e.RemoveComponentRaw(s)
    try:
        e.sound
    except AttributeError:
        print "sound removed successfully"

if 0: #create a new component, hilight
    e = naali.getUserAvatar()
    try:
        e.highlight
    except AttributeError:
        print e.GetOrCreateComponentRaw("EC_Highlight")
        print "created a new Highlight component"

    h = e.highlight
    print type(h), h, h.GetParentEntity()
    
    h.Show()
    #h.Hide()
    
    vis = h.IsVisible()
    if vis:
        print "vis"
    else:
        print "not"
        
if 0: #create a new component, touchable
    e = naali.getUserAvatar()
    try:
        t = e.touchable
    except AttributeError:
        print e.GetOrCreateComponentRaw("EC_Touchable")
        print "created a new Touchable component", e.Id
        t = e.touchable

    print type(t), t, t.GetParentEntity()
    
    def onhover():
        print "hover on avatar"
    t.connect('MouseHover()', onhover)
        
    def onclick():
        print "click on avatar"
    t.connect('Clicked()', onclick)   
        
    #h.Show()
    #h.Hide()
    
    #vis = h.IsVisible()
    #if vis:
    #    print "vis"
    #else:
     #   print "not"


if 0: #the new DynamicComponent with individual attrs etc
    doorid = 2088825623

    e = naali.getEntity(doorid)
    dc = e.getDynamicComponent("door")
    a = dc.GetAttribute("opened")
    print a, type(a)
    dc.SetAttribute("opened", True)
    # Todo: OnChanged() is deprecated
    dc.OnChanged()

    jssrc = dc.GetAttribute("js_src")
    print jssrc

if 0: #create DynamicComponent
    ent = naali.getEntity(1734318933)
    comp = ent.GetOrCreateComponentRaw("EC_DynamicComponent", "hep")
    #d = ent.EC_DynamicComponent
    #d = ent.dynamiccomponent
    print "new DC:", comp
    #d.CreateAttribute("real", "y")
    #print d.SetAttribute('y', 0.5)
    #print d.GetAttribute('y')

if 0: #animation control
    ent = naali.getUserAvatar()
    try:
        ent.animationcontroller
    except AttributeError:
        #ent.GetOrCreateComponentRaw("EC_DynamicComponent")
        print ent, "has no animation controller component"
    
    a = ent.animationcontroller
    print a, dir(a)
    #animname = "Fly"
    animname = "Walk"
    a.EnableAnimation(animname)
    #print a.SetAnimationTimePosition("Walk", 0.2)

    #step with consequent calls
    try:
        r.t
    except: #first run
        r.t = 0
    r.t += 0.1
    print a.SetAnimationTimePosition(animname, r.t % 1)
    
        
if 0: #log level visibility
    r.logDebug("Debug")
    #r.logWarning("Warning") #not implement now, should add i guess
    r.logInfo("Info")

if 0: #local object creation, testing if local previews of .scenes would work
    from PythonQt.QtGui import QVector3D as Vec3
    from PythonQt.QtGui import QQuaternion as Quat

    print "hep"
    e = naali.createMeshEntity("Jack.mesh")
    print e
    e.placeable.Position = Vec3(128, 128, 60)
    e.placeable.Scale = Vec3(5, 5, 5)
    e.placeable.Orientation = Quat(0, 0, 0, 1)

if 0: #createentity directly from the c++ scenemanager where it's a qt slot now
    #s = naali.getDefaultScene()
    #id = s.NextFreeId()
    #ent = s.CreateEntityRaw(id)
    ent = naali.createEntity()
    print "new entity created:", ent, ent.Id

if 0: #running localscene dotscene loader
    import localscene.loader
    localscene.loader = reload(localscene.loader)

    filename = "pymodules/localscene/test.scene"
    localscene.loader.load_dotscene(filename)

    #avatar = r.getEntity(r.getUserAvatarId())
    #print avatar.placeable.Position.toString()

if 0: #loadurl handler import test
    import loadurlhandler
    loadurlhandler = reload(loadurlhandler)
    l = loadurlhandler.LoadURLHandler()
    print l

if 0: #webview as external qt windows, to test how web map javascripts work
    import PythonQt

    try:
        webview = r.webview
    except:
        webview = PythonQt.QtWebKit.QWebView()
        r.webview = webview #is GCd otherwise immediately

    #urlstring = 'http://an.org/'
    urlstring = 'http://www.osgrid.org/elgg/pg/utilities/map'
    #urlstring = 'http://beta.simstad.nl:8010/client/default_map.html'
    url = PythonQt.QtCore.QUrl(urlstring)
    webview.load(url)
    webview.show()

    print r.webview

if 0: #webview as 3dcanvas
    import PythonQt

    try:
        webview = r.webview
    except:
        webview = PythonQt.QtWebKit.QWebView()
        r.webview = webview #is GCd otherwise immediately

    #urlstring = "http://an.org/"    
    urlstring = "http://www.fmi.fi/saa/sadejapi.html"
    url = PythonQt.QtCore.QUrl(urlstring)
    webview.load(url)
    refreshrate = 10
    #webview.show()

    #avid = r.getUserAvatarId()
    #r.applyUICanvasToSubmeshes(avid, [0], webview, refreshrate)

    print webview

if 0: #old PyEntity - doesn't crash when is removed
    try:
        newent = r.newent
    except:
        newent = r.newent = r.createEntity("axes.mesh", 1234567)
        print "Created newent:", newent
    else:
        print "Found newent", newent

    if 0:
        r.removeEntity(newent.id)
        print "Deleted newent"

    print newent.id
    print newent.placeable

if 0:
    del r.newent

if 0: #using Scene::Entity directly. does it crash when i keep a ref and it's removed? no!
    try:
        newent = r.newent
    except:
        newent = r.newent = naali.createEntity()
        print "Created newent:", newent
    else:
        print "Found newent", newent

    if 0:
        r.removeEntity(newent.Id) #uh i'm an idiot, forgot to expose RemoveEntity in SM
        print "Deleted newent"

    print newent.Id
    print newent.GetComponentRaw("EC_Placeable")

if 0: #Scene::Entity CreateEntity with components .. to reimplement createMeshEntity
    #XXX wasn't possible yet. lead into research about adding QPointer support to PythonQt internals etc
    ent = naali.createEntity(["EC_Placeable", "EC_Mesh"])

    ent.mesh.SetPlaceable(ent.placeable) #wants a boost shared_ptr, which we don't have :/
    ent.mesh.SetMesh("axes.mesh")

if 0: #adding components as dynamic properties of Scene::Entity
    ent = naali.getUserAvatar()
    qent = ent.qent
    print qent.dynamicPropertyNames()

    if 0:
        qent.setProperty("myplace", ent.placeable)
        print qent.myplace

    #print dir(qent), type(qent.EC_Placeable), qent.EC_Placeable
    print dir(ent.placeable)
    print "Name:", ent.placeable.Name
    print "objectName:", ent.placeable.objectName

    print "DynProp check:", 'myplace' in qent.dynamicPropertyNames()
    
if 0: #using the dynamic property component getters implemented in core/componentpropertyadder now
    ent = naali.getUserAvatar()
    qent = ent.qent
    print dir(qent)
    print qent.dynamicPropertyNames()
    print qent.placeable

if 0: #getting all entities with a certain component, now directly as the entity objects. works :)
    s = naali.getDefaultScene()
    ents = s.GetEntitiesWithComponentRaw("EC_Placeable")
    for ent in ents:
        print ent.placeable.Position
        
if 0: #estate management uses presence info. websocketserver too
    s = naali.getDefaultScene()
    ents = s.GetEntitiesWithComponentRaw("EC_OpenSimPresence")
    for ent in ents:
        displaystring = ent.opensimpresence.QGetFullName() + "|" + ent.opensimpresence.QGetUUIDString()
        print displaystring

if 1: #start a pythonqt console
    try:
        r.qtconsole
    except:
        r.qtconsole = naali._pythonscriptmodule.CreateConsole()
    
    #show also if was hidden previously
    r.qtconsole.show()
