# 导入maya和arnold的模块
import maya.cmds as cmds
import mtoa.core as core
import os

folder_field = []

def create_window():
    # 检查是否已经存在同名的窗口，如果有就删除
    window_name = "批量导入导出ar代理"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    # 创建一个窗口
    window = cmds.window(title=window_name, widthHeight=(300, 200))

    # 创建一个布局
    layout = cmds.columnLayout(adjustableColumn=True)

    # 创建一个文本标签，提示用户输入文件夹路径
    label = cmds.text(label="请输入你要导出代理文件的文件夹路径:")

    # 创建一个输入框，用来接收用户输入的文件夹路径
    text_field = cmds.textField("folder_path")

    # 创建一个按钮，用来触发导出代理文件的函数
    button = cmds.button(label="Export", command="export_proxy()")

    # 创建一个文本标签，提示用户输入文件夹路径
    label = cmds.text(label="请输入你要导入代理文件的文件夹路径:")

    # 创建一个文本字段，用于输入文件夹路径
    global folder_field
    folder_field = cmds.textField(placeholderText="")

    # 创建一个按钮，用于执行导入代理模型的函数
    button = cmds.button(label="Import", command=lambda x: batch_import_arnold_proxy())


    # 显示窗口
    cmds.showWindow(window)



def batch_import_arnold_proxy():
    # 获取文本字段中的文件夹路径
    folder = cmds.textField(folder_field, query=True, text=True)

    # 使用os.listdir函数来获取文件夹内的所有文件和子文件夹名称
    filelist = os.listdir(folder)

    # 使用列表推导式来筛选出以.ass结尾的文件名称，并使用os.path.join函数来拼接完整的文件路径
    filelist = [os.path.join(folder, fname) for fname in filelist if os.path.splitext(fname)[1] == ".ass"]
    transform_nodes = []
        # 遍历文件列表
    for file in filelist:
        # 创建一个arnold代理节点
        proxy_node = core.createArnoldNode("aiStandIn")

        # 设置代理节点的文件属性为文件路径
        cmds.setAttr(proxy_node + ".dso", file, type="string")

        # 获取代理节点的变换节点，并添加到列表中
        transform_node = cmds.listRelatives(proxy_node, parent=True)[0]
        transform_nodes.append(transform_node)

        # 获取文件名，不包含扩展名
        filename = os.path.splitext(os.path.basename(file))[0]

        # 给文件名添加Shape后缀
        for fileshapename in filename:
            fileshapename = filename + "Shape"

        # 重命名变换节点为文件名
        cmds.rename(transform_node, filename)

        # 将模型名称给到列表mod里
        mod = (filename)

        #选择mod内的模型
        cmds.select(mod)

        # 获取mod内模型的shape节点名称
        backplate = cmds.listRelatives(s=1)[0]

        # 重命名shape节点名称
        cmds.rename(backplate, fileshapename)


    return transform_nodes

def export_proxy():
    # 获取输入框中的文件夹路径
    folder_path = cmds.textField("folder_path", query=True, text=True)
    # 选择要导出的物体
    selection = cmds.ls(sl=True)
    # 遍历每个物体，为每个物体生成一个代理文件
    for obj in selection:
        # 设置代理文件的路径和名称
        proxy_file = folder_path + "/" + obj + "_ass" + ".ass"
        # 设置导出选项，mask=223表示导出灯光、相机、形状和着色器，去掉-compressed表示不压缩
        export_options = "-mask 223;-lightLinks 0;-boundingBox;-shadowLinks 0"
        # 只选择当前的物体
        cmds.select(obj)
        # 调用arnoldExportAss命令，导出代理文件
        cmds.arnoldExportAss(f=proxy_file, mask=223, lightLinks=0, compressed=False, boundingBox=True, shadowLinks=0, s=True)
        # 恢复原来的选择
        cmds.select(selection)

#调用窗口函数
create_window()
