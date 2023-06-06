<template>
  <div>
    <el-table :data="filterTableData" style="width: 100%">
    <el-table-column label="工号" prop="workno" />
    <el-table-column label="姓名" prop="name" />
    <el-table-column label="性别" prop="gender" />
    <el-table-column label="职称" prop="level" />
    <el-table-column align="center">
      <template #header>
        <el-input v-model="search" size="small" placeholder="Type to search" />
      </template>
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
          >Edit</el-button
        >
      </template>
    </el-table-column>
  </el-table>
    </div>

</template>

<script setup>
import { computed, ref } from 'vue'
import {Teachers} from '@/api/teacher'
const search = ref('')

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return TableData.value
  } else {
    return TableData.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

const handleEdit = (index, row) => {
  console.log(index, row)
}

// 创建一个响应式变量
var TableData = ref([]);
getTeachers();

function getTeachers() {
    // 使用api方法
    Teachers()
        .then(res => {
            if (res.data.code === 200) {
                TableData.value = res.data.data.items;
            } else {
                alert("教师数据获取失败")
            }
        })
}


</script>
