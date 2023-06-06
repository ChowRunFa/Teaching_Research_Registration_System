<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="课程" name="first">
      添加课程信息 <br><br>
       <el-form :model="form" label-width="120px">

          <!-- 选择课程表格 -->
    <el-form-item label="选择课程">

      <el-table :data="pagedTableData" style="width: 100%">
        <el-table-column prop="id" label="课程ID" />
        <el-table-column prop="name" label="课程名称" />
        <el-table-column prop="hours" label="学时" />
        <el-table-column prop="property" label="性质" />
        <el-table-column label="操作">
          <template #header>
        <el-input v-model="search" size="default" placeholder="输入课程名搜索"  style="width: 50%;"/>
      </template>
          <template v-slot="scope">
            <el-button type="text" @click="selectCourse(scope.row)">选择</el-button>
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

    </el-form-item>

             <!-- 显示当前选中的课程 -->
    <el-form-item label="当前选中的课程">
      <el-input v-model="selectedCourse" disabled></el-input>
    </el-form-item>

  <el-row :gutter="25" style="margin-top: 10px;">

    <el-col :span="5">
      <el-form-item label="授课教师">
<el-select v-model="newAuthor.workno" placeholder="选择任课教师" @change="handleSelectChange">
  <el-option v-for="option in worknoOptions" :key="option.workno" :label="option.name" :value="option.workno" :data-option="option" />
</el-select>
      </el-form-item>
    </el-col>

    <el-col :span="5">
    <el-form-item label="学年">
        <el-date-picker
          v-model="newAuthor.year"
          type="year"
          placeholder="选择一个学年"
          style="width: 100%"
        />
    </el-form-item>
    </el-col>

    <el-col :span="5">
      <el-form-item label="学期">
<el-select v-model="newAuthor.semester" placeholder="选择一个学期" @change="handleSelectChange">
      <el-option label="春季学期" value="1" />
      <el-option label="夏季学期" value="2" />
      <el-option label="秋季学期" value="3" />
</el-select>
      </el-form-item>
    </el-col>


    <el-col :span="4">
      <el-form-item label="承担学时">
        <el-input v-model.number="newAuthor.hours" type="number" placeholder="输入承担学时" />
      </el-form-item>
    </el-col>

    <el-col :span="5" :offset="0.5">
    <el-button type="primary" plain @click="addAuthor">添加</el-button>
    </el-col>
  </el-row>

         <el-form-item label="作者列表">
  <el-table :data="form.teachings" style="width: 100%">
    <el-table-column prop="workno" label="工号" />
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="gender" label="性别" />
    <el-table-column prop="level" label="职称" />
    <el-table-column prop="year" label="学年" />
    <el-table-column prop="semester" label="学期" />
    <el-table-column prop="hours" label="承担学时" />
    <el-table-column label="操作">
      <template v-slot="scope">
        <el-button type="text" @click="removeAuthor(scope.$index)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

</el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">提交</el-button>
      <el-button>取消</el-button>
    </el-form-item>

  </el-form>
    </el-tab-pane>

  </el-tabs>
</template>
<script  setup>
import { computed,ref } from 'vue'
import { reactive } from 'vue'
import {Teachers} from '@/api/teacher'
import { PostCourse } from '@/api/course';
import { Courses } from '@/api/course';

const activeName = ref('first')
// 定义响应式变量 courseOptions
const courseOptions = ref([])
// 定义响应式变量 selectedCourse，用于显示当前选中的课程信息
const selectedCourse = ref('')
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
getCourseOptions()

const handleClick = (tab, event) => {
  console.log(tab, event)
}

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return courseOptions.value
  } else {
    return courseOptions.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
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

// do not use same name with ref
const form = reactive(
    {
      id: null,
      name: null,
      hours: null,
      property: null,
      teachings:[]
    })


function getCourseOptions() {
  // 使用 Courses API 获取课程列表
  Courses()
    .then(res => {
      if (res.data.code === 200) {
        courseOptions.value = res.data.data.items
      } else {
        alert("课程数据获取失败")
      }
    })
}


// 处理选择课程的事件
const selectCourse = (course) => {
  // 将课程信息填充到表单中
  form.id = course.id
  form.name = course.name
  form.hours = course.hours
  form.property = course.property

  // 更新 selectedCourse 变量，以显示当前选中的课程信息
  selectedCourse.value = `${course.id} - ${course.name}`
}




// 创建一个响应式变量
var worknoOptions = ref([]);
getTeachers();

function getTeachers() {
    // 使用api方法
    Teachers()
        .then(res => {
            if (res.data.code === 200) {
                worknoOptions.value = res.data.data.items;
            } else {
                alert("教师数据获取失败");
            }
        })
}

const newAuthor = reactive({
        workno:null,
        name: null,
        gender: null,
        level: null,
        year:null,
        semester:null,
        hours:null
})

const addAuthor = () => {
  // 将日期对象转换为只包含年份的整数
  const year = newAuthor.year ? new Date(newAuthor.year).getFullYear() : null;

  // 创建新教师对象
  const newTeacher = {
    workno: newAuthor.workno,
    name: newAuthor.name,
    gender: newAuthor.gender,
    level: newAuthor.level,
    year: year,
    semester: newAuthor.semester,
    hours: newAuthor.hours
  };

  // 将新教师对象添加到表单数据中
  form.teachings.push(newTeacher);

  // 清空表单数据
  newAuthor.workno = null;
  newAuthor.name = null;
  newAuthor.gender = null;
  newAuthor.level = null;
  newAuthor.year = null;
  newAuthor.semester = null;
  newAuthor.hours = null;
};

const removeAuthor = index => {
  form.charges.splice(index, 1)
}

const handleSelectChange = (value) => {
const option = worknoOptions.value.find(option => option.workno === value)
  if (option) {
    newAuthor.workno = value
    newAuthor.name = option.name
    newAuthor.gender = option.gender
    newAuthor.level = option.level
    // 将 option 的其他属性也赋给 newAuthor
    Object.assign(newAuthor, option)
  }
}


const onSubmit = () => {
        console.log(form)
        // console.log(data.corresponding_author)
  PostCourse(form)
  .then(res => {
    if (res.data.code === 200) {
           alert(res.data.msg)
  }else {
           alert(res.data.msg)
    }
  })
}

</script>
<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
