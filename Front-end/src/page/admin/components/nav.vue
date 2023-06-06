<style scoped>
.el-row{
  height: 100%;
}

.el-menu{
  border-right: 1px solid #f5f1f1;
}
.el-aside{
  border-right: 1px solid #f5f1f1;
}
</style>

<template>
  <el-aside width="200px">
    <el-row class="tac">
      <el-col>
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
        >
          <el-menu-item index="1" @click="goPage('teacherinfo')">
            <i class="el-icon-s-order"></i>
            <span slot="title">信息总览</span>
          </el-menu-item>

          <el-menu-item index="2" @click="goPage('manage')">
            <i class="el-icon-s-order"></i>
            <span slot="title">论文登记</span>
          </el-menu-item>

          <el-menu-item index="3" @click="goPage('addproject')">
            <i class="el-icon-s-order"></i>
            <span slot="title">项目登记</span>
          </el-menu-item>

          <el-menu-item index="4" @click="goPage('addcourse')">
            <i class="el-icon-s-order"></i>
            <span slot="title">课程登记</span>
          </el-menu-item>

          <el-menu-item index="5" @click="goPage('teacher')">
            <el-icon class="el-icon-s-order"></el-icon>
            <span slot="title">教师信息</span>
          </el-menu-item>

          <el-menu-item index="6" @click="goPage('paper')">
          <el-icon class="el-icon-s-order"></el-icon>
            <span slot="title">论文信息</span>
          </el-menu-item>

          <el-menu-item index="7" @click="goPage('project')">
          <el-icon class="el-icon-s-order"></el-icon>
            <span slot="title">项目信息</span>
          </el-menu-item>

          <el-menu-item index="8" @click="goPage('course')">
          <el-icon class="el-icon-s-order"></el-icon>
            <span slot="title">课程信息</span>
          </el-menu-item>


        </el-menu>
      </el-col>
    </el-row>
  </el-aside>
</template>

<script>
var $this = {};
export default {
  data() {
    return {};
  },
  beforeCreate() {
    $this = this;
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },

    goPage(link) {
      if (link === "teacherinfo") {
        $this.$router.push("/admin/teacherinfo").catch(error => error);
      } else if (link === "manage") {
        $this.$router.push("/admin/manage").catch(error => error);
      } else if (link === "addproject") {
        $this.$router.push("/admin/addproject").catch(error => error);
      } else if (link === "addcourse") {
        $this.$router.push("/admin/addcourse").catch(error => error);
      } else if (link === "teacher") {
        $this.$router.push("/admin/teacher").catch(error => error);
      } else if (link === "paper") {
        $this.$router.push("/admin/paper").catch(error => error);
      }else if (link === "project") {
        $this.$router.push("/admin/project").catch(error => error);
      }else if (link === "course") {
        $this.$router.push("/admin/course").catch(error => error);
      } else {

      }
    }
  }
};
</script>
