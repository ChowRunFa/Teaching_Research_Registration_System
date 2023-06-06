// 导入request
import request from '@/utils/request'
// 导出登录方法
export function Papers(){
    return request.get("/api/papers")
}


export function DelPaper(id){
    return request.delete('/api/del/paper/'+id)
}

export function PostPaper(form){
    return request.post('/api/add/paper',form)
}

