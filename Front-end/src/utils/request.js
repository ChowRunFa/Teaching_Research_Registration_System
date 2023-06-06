import axios from 'axios';
//����axiosʵ��
const request = axios.create(
    {
        baseURL : 'http://localhost:5000',
        timeout : 5000
    }
)
//�����������
request.interceptors.request.use(function (config){
    //�������ͷ
  config.headers.Authorization = "Bearer "+localStorage.getItem("token");
      return config;
})

//����
export default request