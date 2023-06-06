import axios from 'axios';
//创建axios实例
const request = axios.create(
    {
        baseURL : 'http://localhost:5000',
        timeout : 5000
    }
)
//添加请求拦截
request.interceptors.request.use(function (config){
    //添加请求头
  config.headers.Authorization = "Bearer "+localStorage.getItem("token");
      return config;
})

//导出
export default request