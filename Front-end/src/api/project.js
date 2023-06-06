// 导入request
import request from '@/utils/request'
// 导出登录方法
export function Projects(){
    return request.get("/api/projects")
}
export function DelProject(id){
    return request.delete("/api/del/project/"+id)
}

export function PostProject(form){
    return request.post('/api/add/project',form)
}
