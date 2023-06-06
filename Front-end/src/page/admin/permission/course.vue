<template>
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
          <el-tab-pane label="新建课程" name="first">
      新建课程信息 <br><br>
       <el-form :model="form" label-width="120px">
    <el-form-item label="课程编号">
      <el-input v-model="form.id"  placeholder="输入课程编号"/>
    </el-form-item>

         <el-form-item label="课程名称">
      <el-input v-model="form.name" placeholder="输入课程名称"/>
    </el-form-item>

         <el-form-item label="课程学时">
      <el-input v-model="form.hours" type="number" placeholder="输入课程学时"/>
    </el-form-item>

    <el-form-item label="课程类型">
      <el-select v-model="form.property" placeholder="选择课程类型">
      <el-option label="必修" value="1" />
      <el-option label="选修" value="2" />
      <el-option label="公选" value="3" />
      <el-option label="通识" value="4" />
      </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">创建</el-button>
      <el-button>取消</el-button>
    </el-form-item>
  </el-form>
          </el-tab-pane>

          <el-tab-pane label="查看课程" name="second">
             <el-table :data="pagedTableData" style="width: 100%">
      <el-table-column label="课程号" prop="id" />
      <el-table-column label="课程名" prop="name" />
      <el-table-column label="课程学时" prop="hours" />
      <el-table-column label="课程性质" prop="property" />
      <el-table-column align="right">
        <template #header>
        <el-input v-model="search" size="small" placeholder="输入课程名搜索" />
      </template>
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
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
          </el-tab-pane>
    </el-tabs>

</template>

<script setup>
import { computed,reactive ,ref } from 'vue'
import { Courses, DelCourse, NewCourse} from '@/api/course'

const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const activeName = ref('first')
// 创建一个响应式变量
const tableData = ref([])
getCourses()

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return tableData.value
  } else {
    return tableData.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

const form = reactive(
    {
      id: null,
      name: null,
      hours: null,
      property: null
    })




function getCourses() {
  // 使用api方法获取论文数据
  Courses().then(res => {
    if (res.data.code === 200) {
      tableData.value = res.data.data.items
    } else {
      alert('论文数据获取失败')
    }
  })
}

const handleClick = (tab, event) => {
  console.log(tab, event)
}

const handleEdit = (index, row) => {
  console.log(index, row)
}

const handleDelete = (index, row) => {
  console.log(index, row)
  DelCourse(row.id).then(res => {
    if (res.data.code === 200) {
      alert('删除成功')
      getCourses()
    } else {
      alert('删除失败')
    }
  })
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const onSubmit = () => {
        console.log(form)
        // console.log(data.corresponding_author)
  NewCourse(form)
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