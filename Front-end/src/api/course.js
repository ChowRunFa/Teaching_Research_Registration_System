// 导入request
import request from '@/utils/request'
// 导出登录方法
export function Courses(){
    return request.get("/api/courses")
}


export function DelCourse(id){
    return request.delete('/api/del/course/'+id)
}

export function PostCourse(form){
    return request.post('/api/add/course',form)
}

export function NewCourse(form){
    return request.post('/api/new/course',form)
}



