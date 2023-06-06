<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="项目" name="first">
      添加项目信息 <br><br>
       <el-form :model="form" label-width="120px">
    <el-form-item label="项目序号">
      <el-input v-model="form.id" type="number" placeholder="输入项目序号"/>
    </el-form-item>

         <el-form-item label="项目名称">
      <el-input v-model="form.name" placeholder="输入项目名称"/>
    </el-form-item>

         <el-form-item label="项目来源">
      <el-input v-model="form.source" placeholder="输入项目来源"/>
    </el-form-item>

         <el-form-item label="项目经费">
      <el-input type="number" v-model="form.totalfund" placeholder="输入项目总经费" style="width: 15%;"/>
    </el-form-item>

    <el-form-item label="项目类型">
      <el-select v-model="form.type" placeholder="选择项目类型">
<el-option label="国家级项目" value="1" />
<el-option label="省部级项目" value="2" />
<el-option label="市厅级项目" value="3" />
<el-option label="企业合作项目" value="4" />
<el-option label="其它类型项目" value="5" />
      </el-select>
    </el-form-item>



    <el-form-item label="立项时间">
      <el-col :span="3">
        <el-date-picker
          v-model="form.startyear"
          type="date"
          placeholder="选择项目立项时间"
          style="width: 100%"
        />
      </el-col>
    </el-form-item>

         <el-form-item label="结项时间">
      <el-col :span="3">
        <el-date-picker
          v-model="form.endyear"
          type="date"
          placeholder="选择项目结项时间"
          style="width: 100%"
        />
      </el-col>
    </el-form-item>

  <el-row :gutter="25" style="margin-top: 10px;">

    <el-col :span="5">
      <el-form-item label="项目人员">
<el-select v-model="newAuthor.workno" placeholder="选择教师" @change="handleSelectChange">
  <el-option v-for="option in worknoOptions" :key="option.workno" :label="option.name" :value="option.workno" :data-option="option" :disabled="form.charges.some(author => author.workno === option.workno)"/>
</el-select>
      </el-form-item>
    </el-col>

    <el-col :span="4">
      <el-form-item label="排名">
        <el-input v-model.number="newAuthor.ranking" type="number" placeholder="输入排名" />
      </el-form-item>
    </el-col>

    <el-col :span="4">
      <el-form-item label="经费">
        <el-input v-model.number="newAuthor.fund" type="number" placeholder="输入经费" />
      </el-form-item>
    </el-col>

    <el-col :span="8" :offset="0.5">
    <el-button type="primary" plain @click="addAuthor">添加</el-button>
    </el-col>
  </el-row>

         <el-form-item label="作者列表">
  <el-table :data="form.charges" style="width: 100%">
    <el-table-column prop="workno" label="工号" />
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="gender" label="性别" />
    <el-table-column prop="level" label="职称" />
    <el-table-column prop="ranking" label="排名" />
    <el-table-column prop="fund" label="经费" />
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
import { PostProject } from '@/api/project';

const activeName = ref('first')

const handleClick = (tab, event) => {
  console.log(tab, event)
}

// do not use same name with ref
const form = reactive({
    id: null,
    name: null,
    source: null,
    type: null,
    startyear: null,
    endyear: null,
    totalfund: null,
    charges:[]
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
                ranking:null,
                fund:null
})

const addAuthor = () => {
  form.charges.push({ ...newAuthor });
  newAuthor.workno = null;
  newAuthor.name = null;
  newAuthor.gender = null;
  newAuthor.level = null;
  newAuthor.ranking = null;
  newAuthor.fund = null;
}

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
  const data = {
    id: form.id,
    name: form.name,
    source: form.source,
    type: form.type,
    startyear: form.startyear,
    endyear: form.endyear,
    totalfund: form.totalfund,
    charges: form.charges
  }
        console.log(form)
        // console.log(data.corresponding_author)
  PostProject(form)
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
