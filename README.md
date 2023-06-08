# Teaching_Research_Registration_System
### 技术栈：Flask+MySQL+Vue3.0+ElementPlus+Axios
### 使用前后端分离的开发方式
### 项目介绍：USTC 数据库系统与应用 2023春 Lab3 第三次实验
- Front-end：Vue前端项目
- Back-end：Flask后端项目
- Lab_Introduction: 实验内容介绍

## 2023/6/3 V1.0
### 初始页面
 ![ZK$T@S WLG%BFNF6HCN${YI](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/efdf6941-db1c-48a1-ada9-26f0e06ba739)
 ![5ZH)DIGMTX}AP%8UE 35HC](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/6a8bbe4f-4ee3-44d2-bb40-9fee80e68328)

## 2023/6/4 V1.0.1
### 修改首页 添加基础查询/删除操作表格
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/81f7efae-4131-42d4-8390-1b5cbceff420)
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/7c3a059c-5353-45d0-8867-a427ea689b3f)

## 2023/6/5 V1.1.0
### 1.添加信息登记功能：论文信息上传表单  (后续开发基于这个基础会更快)
### 2.论文/项目表格分页
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/2b3a72de-11a8-4308-a2b5-85069a6ad617)
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/631c0c5c-ff55-4f87-a861-ec9c3978a16b)

## 2023/6/6 V1.2.0
### 1.将信息登记拆分  分别为论文登记  项目登记 课程登记   
### 2.添加信息总览页面  展示每个教师的基本信息以及教学 项目 科研情况
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/65c73464-174c-4cfe-9df9-3c208d4ae610)
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/ffcf3119-e67f-4d34-8016-7a0a8e569c37)
## 2023/6/7 V1.3.0
### 1. 添加课程登记功能 
#### - 逻辑：GET请求数据库已有的所有课程，选中一个已有的课程，再GET请求所有数据库已有的教师，再给该教师分配对应课程的学年学期学时，再POST表单提交，后端接口负责检查学时约束
#### - 选择课程支持通过搜索课程名来筛选，这样在课程较多时，不用逐页手动寻找课程(费眼) 
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/72a51112-0570-4f9c-89a3-93d8e8d8a176)
### 2. 添加上传论文信息 项目信息等的各个表单中，禁用已选教师的功能
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/f7703d51-eada-4869-9342-fd783406b21d)
### 3. 添加新建课程以及查看课程功能(此功能不知道为什么此前似乎被忽略了QAQ)
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/08757f94-1b5d-4cab-b760-48901243db90)
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/4e98f214-5156-4bff-8fb1-3dfff56967b2)
## 2023/6/8 V1.4.0
### 1. 科研信息总览功能
###  - 逻辑：首先获取教师列表，再根据教师与论文、项目、课程的关系进行多表联合查询，将每个教师所属的信息添加到该教师下，最终得到一个列表，每个列表的元素是一个教师信息的字典集
###  - 功能：1. 初始化页面获取所有教师的信息，可以选择一个教师直接查看该教师的教学科研信息 2. 教师信息同样采用分页的方式，避免一页过多教师，并且支持搜索教师名查找教师 3.支持查找所有时间的数据以及指定时间的数据，通过一个开关控制 4. 得到的教学科研信息支持打印pdf
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/02b60cc0-9d34-4619-86c8-23326344039c)
![image](https://github.com/ChowRunFa/Teaching_Research_Registration_System/assets/97417202/3b131c1b-c3fa-40d0-9cd9-8c7ef6281ad2)

