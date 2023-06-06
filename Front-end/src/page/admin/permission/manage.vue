<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="论文" name="first">
      添加论文信息 <br><br>
       <el-form :model="form" label-width="120px">
    <el-form-item label="论文序号">
      <el-input v-model="form.id" type="number" placeholder="输入论文序号"/>
    </el-form-item>

         <el-form-item label="论文标题">
      <el-input v-model="form.title" placeholder="输入论文标题"/>
    </el-form-item>

         <el-form-item label="发表源址">
      <el-input v-model="form.source" placeholder="输入论文发表源址"/>
    </el-form-item>

    <el-form-item label="论文类型">
      <el-select v-model="form.type" placeholder="选择论文类型">
      <el-option label="Full Paper" value="1" />
      <el-option label="Short Paper" value="2" />
      <el-option label="Poster Paper" value="3" />
      <el-option label="Demo Paper" value="4" />
      </el-select>
    </el-form-item>

         <el-form-item label="论文级别">
      <el-select v-model="form.level" placeholder="选择论文级别">
      <el-option label="CCF-A" value="1" />
      <el-option label="CCF-B" value="2" />
      <el-option label="CCF-C" value="3" />
      <el-option label="中文CCF-A" value="4" />
      <el-option label="中文CCF-B" value="5" />
      <el-option label="无级别" value="6" />
      </el-select>
    </el-form-item>

    <el-form-item label="发表时间">
      <el-col :span="11">
        <el-date-picker
          v-model="form.year"
          type="date"
          placeholder="选择论文发表时间"
          style="width: 100%"
        />
      </el-col>
    </el-form-item>

  <el-row :gutter="25" style="margin-top: 10px;">

    <el-col :span="5">
      <el-form-item label="选择作者">
<el-select v-model="newAuthor.workno" placeholder="选择教师" @change="handleSelectChange">
  <el-option v-for="option in worknoOptions" :key="option.workno" :label="option.name" :value="option.workno" :data-option="option" :disabled="form.authors.some(author => author.workno === option.workno)" />
</el-select>

      </el-form-item>
    </el-col>
    <el-col :span="4">
      <el-form-item label="排名">
        <el-input v-model.number="newAuthor.ranking" type="number" placeholder="输入排名" />
      </el-form-item>
    </el-col>
    <el-col :span="8" :offset="0.5">
    <el-button type="primary" plain @click="addAuthor">添加</el-button>
    </el-col>
  </el-row>

         <el-form-item label="作者列表">
  <el-table :data="form.authors" style="width: 100%">
    <el-table-column prop="workno" label="工号" />
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="gender" label="性别" />
    <el-table-column prop="level" label="职称" />
    <el-table-column prop="ranking" label="排名" />
    <el-table-column label="操作">
      <template v-slot="scope">
        <el-button type="text" @click="removeAuthor(scope.$index)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

</el-form-item>

    <el-form-item label="通讯作者">
    <el-select v-model="form.corresponding_author.workno" placeholder="选择通讯作者工号" :onUpdate:modelValue="onAuthorChange">
      <el-option v-for="(author, index) in form.authors" :key="index" :label="author.workno" :value="index" />
    </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">提交</el-button>
      <el-button>取消</el-button>
    </el-form-item>

  </el-form>
    </el-tab-pane>

    <el-tab-pane label="Config" name="second">
      Config
    </el-tab-pane>

    <el-tab-pane label="Role" name="third">
      Role
    </el-tab-pane>

    <el-tab-pane label="Task" name="fourth">
      Task
    </el-tab-pane>
  </el-tabs>
</template>
<script  setup>
import { ref } from 'vue'
import { reactive } from 'vue'
import {Teachers} from '@/api/teacher'
import { PostPaper } from '@/api/paper';

const activeName = ref('first')

const handleClick = (tab, event) => {
  console.log(tab, event)
}

// do not use same name with ref
const form = reactive({
  id: null,
  title: '',
  source: '',
  year: null,
  type: null,
  level: null,
  authors: [],
  corresponding_author: {}
  })


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
                workno: '',
                name: '',
                gender: null,
                level: null,
                ranking:null
})

const addAuthor = () => {
  form.authors.push({ ...newAuthor });
  newAuthor.workno = null;
  newAuthor.name = null;
  newAuthor.gender = null;
  newAuthor.level = null;
  newAuthor.ranking = null;
}

const removeAuthor = index => {
  form.authors.splice(index, 1)
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
    const correspondingAuthorIndex = ref(null);
    const onAuthorChange = (value) => {
      const author = form.authors[value];
      correspondingAuthorIndex.value = value;
      form.corresponding_author = { ...author };
    };


const onSubmit = () => {

        console.log(form)
        // console.log(data.corresponding_author)
  PostPaper(form)
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
