<template>
  <div>
    <el-table :data="pagedTableData" style="width: 100%">
      <el-table-column label="项目号" prop="id" />
      <el-table-column label="项目名称" prop="name" />
      <el-table-column label="项目来源" prop="source" />
      <el-table-column label="项目类型" prop="type" />
      <el-table-column label="总经费" prop="totalfund" />
      <el-table-column label="开始年份" prop="startyear" />
      <el-table-column label="结束年份" prop="endyear" />
      <el-table-column align="right">
                <template #header>
        <el-input v-model="search" size="small" placeholder="输入项目名搜索" />
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
import { Projects, DelProject } from '@/api/project'

const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 创建一个响应式变量
const tableData = ref([])
getProjects()

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim().toLowerCase()
  if (keyword === '') {
    return tableData.value
  } else {
    return tableData.value.filter(item => {
      const name = item.name ? item.name.toLowerCase() : ''
      return name.includes(keyword)
    })
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

function getProjects() {
  // 使用api方法获取项目数据
  Projects().then(res => {
    if (res.data.code === 200) {
      tableData.value = res.data.data.items
    } else {
      alert('项目数据获取失败')
    }
  })
}

const handleEdit = (index, row) => {
  console.log(index, row)
}

const handleDelete = (index, row) => {
  console.log(index, row)
  DelProject(row.id).then(res => {
    if (res.data.code === 200) {
      alert('删除成功')
      getProjects()
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