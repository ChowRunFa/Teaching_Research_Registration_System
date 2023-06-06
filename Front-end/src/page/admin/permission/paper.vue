<template>
  <div>
    <el-table :data="pagedTableData" style="width: 100%">
      <el-table-column label="序号" prop="id" />
      <el-table-column label="标题" prop="title" />
      <el-table-column label="发表源" prop="source" />
      <el-table-column label="年份" prop="year" />
      <el-table-column label="类型" prop="type" />
      <el-table-column label="级别" prop="level" />
      <el-table-column align="right">
        <template #header>
        <el-input v-model="search" size="small" placeholder="输入论文标题搜索" />
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
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Papers, DelPaper } from '@/api/paper'

const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 创建一个响应式变量
const tableData = ref([])
getPapers()

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return tableData.value
  } else {
    return tableData.value.filter(item => item.title.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

function getPapers() {
  // 使用api方法获取论文数据
  Papers().then(res => {
    if (res.data.code === 200) {
      tableData.value = res.data.data.items
    } else {
      alert('论文数据获取失败')
    }
  })
}

const handleEdit = (index, row) => {
  console.log(index, row)
}

const handleDelete = (index, row) => {
  console.log(index, row)
  DelPaper(row.id).then(res => {
    if (res.data.code === 200) {
      alert('删除成功')
      getPapers()
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
</script>