// ����request
import request from '@/utils/request'
// ������¼����
export function Teachers(){
    return request.get("/api/teachers")
}

