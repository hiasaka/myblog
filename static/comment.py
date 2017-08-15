def comment_tree(comment_list):
    ##创建一个div标签
    comment_str="<div class='comment' style='margin-left:30px'>"
    ##遍历comment_list
    for row in comment_list:
        tpl="<div class='content'>%s</div>"%(row['content'])  ##添加一个div标签，作为内容
        ##<div class='comment'>
        ##  <div class ='content' >
        comment_str +=tpl
        if row['child']:
            child_str=comment_tree(row['child'])
            comment_str +=child_str
    comment_str += '</div>'

    return comment_str




