// ����request
import request from '@/utils/request'
// ������¼����
export function Login(data){
    return request.post("/api/login",data)
}

export function teacherInfo(){
    return request.get("/api/teacherInfo")
}

