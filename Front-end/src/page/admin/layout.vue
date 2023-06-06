<style>
.el-main {
  background-color: #f5f7f9;
}

.el-header,
.el-footer {
  background-color: white;
  box-sizing: border-box;
  border-bottom: 1px solid #f5f1f1;
}

.el-container {
  height: 100%;
}
</style>

 <template>
  <el-container>
    <!-- header部分 -->
    <el-header>
      <navtop></navtop>
    </el-header>
    <el-container>
       <!-- aside部分 -->
      <leftNav></leftNav>
      <el-main>
         <!-- main部分 -->

        <router-view/>
      </el-main>
    </el-container>
  </el-container>
</template>


 <script>
import navtop from "./components/nav-top.vue";
import leftNav from "./components/nav.vue";
export default {
  components: {
    navtop,
    leftNav
  },
  data() {
    return {};
  },
  methods: {}
};
</script>
