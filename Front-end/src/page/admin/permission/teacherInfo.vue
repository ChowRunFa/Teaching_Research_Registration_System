<template>
  <div class="container">
    <el-table :data="pagedTableData" style="width: 100%" @row-click="selectTeacher">
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="gender" label="性别">
        <template #default="{ row }">
          {{ row.gender === 1 ? "男" : "女" }}
        </template>
      </el-table-column>
      <el-table-column prop="level" label="职称"></el-table-column>
      <el-table-column prop="workno" label="工号"></el-table-column>
              <el-table-column label="操作">
          <template #header>
        <el-input v-model="search" size="default" placeholder="输入教师名称搜索"  style="width: 50%;"/>
      </template>
          <template v-slot="scope">
            <el-button type="text" >查看</el-button>
          </template>
        </el-table-column>
    </el-table>
<el-pagination
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      :total="filterTableData.length"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    />
<el-container v-if="selectedTeacher">
  <el-main>
    <el-card>
      <div  class="teacher-details" id="teacher-details-container">
        <div class="section">
          <h1 class="section-title">{{ selectedTeacher.name }} 的详细信息</h1>
              <div style="display: flex; justify-content: flex-end;">
      <el-button type="primary" @click="printPDF">保存为PDF</el-button>
    </div>
          <div class="section-content">
            <div class="subsection">
              <h2 class="subsection-title">个人信息</h2>
                          <hr class="divider">
  <table class="teacher-info">
    <tr>
      <th>姓名</th>
      <td>{{ selectedTeacher.name }}</td>
    </tr>
    <tr>
      <th>性别</th>
      <td>{{ selectedTeacher.gender === 1 ? "男" : "女" }}</td>
    </tr>
    <tr>
      <th>职称</th>
      <td>{{ selectedTeacher.level }}</td>
    </tr>
    <tr>
      <th>工号</th>
      <td>{{ selectedTeacher.workno }}</td>
    </tr>
  </table>
            </div>
            <div class="subsection">
              <h2 class="subsection-title">教学情况</h2>
                          <hr class="divider">
               <ol class="centered-list">
                <li v-for="(course, index) in selectedTeacher.courseInfo" :key="index">
                  {{ course.name }} ({{ course.hours }}学时)
                </li>
              </ol>
            </div>
            <div class="subsection">
              <h2 class="subsection-title">论文发表情况</h2>
                          <hr class="divider">
               <ol class="centered-list">
                <li v-for="(paper, index) in selectedTeacher.paperInfo" :key="index">
                  {{ paper.title }}. {{ paper.source }}. {{ paper.year }} ({{ paper.level }}级)
                </li>
              </ol>
            </div>

            <div class="subsection">
              <h2 class="subsection-title">项目承担情况</h2>
                          <hr class="divider">
               <ol class="centered-list">
                <li v-for="(project, index) in selectedTeacher.projectInfo" :key="index">
                  {{ project.name }}. {{ project.source }}. {{ project.startyear }}-{{ project.endyear }} ({{ project.type }}类项目)
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </el-main>

</el-container>

  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import {teacherInfo} from "@/api/user"


const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const items = ref([])
getInfo()

function getInfo() {
  // 使用api方法获取论文数据
  teacherInfo().then(res => {
    if (res.data.code === 200) {
      items.value = res.data.data.items
    } else {
      alert('数据获取失败')
    }
  })
}

  const selectedTeacher = ref(null);

    function selectTeacher(teacher) {
      selectedTeacher.value = teacher;
    }


    // 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return items.value
  } else {
    return items.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

 const printPDF = () => {
  // 定义打印样式
  let printStyle = `
    <style>
      @media print {
        #teacher-details-container {
          position: static !important;
        }
        .el-button {
          display: none !important;
        }
      }
    </style>
  `;

  // 获取<el-container>的HTML内容
  let containerHtml = document.getElementById('teacher-details-container').innerHTML;

  // 创建一个新的窗口，打印HTML内容
let printWindow = window.open('www.xxx.com', '_blank');
  printWindow.document.write(printStyle + containerHtml);
  printWindow.print();
  printWindow.close();
}
</script>

<style>
.container {
  margin: 20px;
}

.section {
  margin-top: 30px;
  margin-bottom: 30px;
}
p{
            margin:1em 0;
            padding:0 0 0 2em;
            text-indent:-1.5em;
            font:normal normal 16px/1.6em SimSun-ExtB;
            color:#000;
        }

.section-title {
  text-align: center;
  font-size: 30px;
  font-weight: bold;
}

.section-content {
  padding: 20px;
}

.subsection {
  margin-top: 20px;
  margin-bottom: 20px;
}

.subsection-title {
  font-size: 24px;
  font-weight: bold;
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin-top: 30px;
  margin-bottom: 30px;
}

.centered-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
}

.centered-list li {
  text-align: center;
  padding: 5px;
}


.teacher-info {
  border-collapse: collapse;
}
.teacher-info th, .teacher-info td {
  border: 1px solid black;
  padding: 8px;
}
.teacher-info th {
  background-color: #f2f2f2;
}
</style>