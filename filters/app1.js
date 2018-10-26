/*const vm = new Vue({
    el: '#app',
    data: {
      results: []
    },
    mounted() {
      axios.get("https://api.nytimes.com/svc/topstories/v2/home.json?api-key=2efcc4b0db5b4859979baa0f40156792")
      .then(response => {this.results = response.data.results})
      //axios.get("http://127.0.0.1:5000/")
      //.then(response => {this.results = response.data})
      //console.log(results)
    }
  });*/

  //import Vue from 'vue'
  //import vSelect from 'vue-select'
  
const SECTIONS = "Development, Infrastructure, Data Science";
const subDev = "Web, Mobile";
const subInf = "ERP, IT Admin/Services";
const subDs = "Big Data, Business Intelligence, Machine Learning";
const devWeb = "Fullstack, Backend, Frontend"
const class_buttons = "btn btn-primary, btn btn-info, btn btn-warning"
var cat1 = 50;
var cat2 = 30;
var cat3 = 20;
var total = 0;
var currentdev = 0;
var currentinf = 0;
var currentds = 0;
var thestyle = [{group: "Development", button: "btn btn-primary", width: "width:", count: this.catdev, pix:"%"}, {group: "Infrastructure", button:"btn btn-info", width: "width:", count: cat2, pix:"%"}, {group:"Data Science", button: "btn btn-warning", width: "width:", count: cat3, pix:"%"}]


    //let url = section === "home"? buildUrl(section) : buildUrl(section) + "/" + sub;
    //let url = buildUrl(section) + "/Web";
    


//var country_selected = document.getElementById("Sub");

const BaseUrl = "http://127.0.0.1:5000/";
const searchBaseUrl = "http://127.0.0.1:5000/search/";


function buildUrl(url) {
    
    return BaseUrl + url
}

function searchUrl(url) {
    
    return searchBaseUrl + url
}

Vue.component('v-select', VueSelect.VueSelect);

Vue.component('news-list', {
    props: ['results'],
    template: `
        <section>
            <table class="ui very basic padded striped four column table accordion">
                        
                        <tbody>
                            <div v-for="posts in processedPosts">
                                <div v-for="post in posts">
                                <hr>
                                
                                    <tr>
                                        
                                        <td>
                                            <div class="title">
                                            <a :href="post.url" target="_blank"><b>{{ post.title }}</b></a>
                                            </div>
                                            
                                            <div class="content">
                                                <div class="ui relaxed divided items">
                                                    <div class="item">
                                                        <div class="description">
                                                            {{ post.description.slice(0,350) }}
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="ui relaxed divided items">
                                                    <div class="item">
                                                        <div class="description">
                                                            Category: <b>{{ post.bereich.group }}</b>
                                                        </div>
                                                        <div class="description">
                                                        
                                                            Sub-Category: <b>{{ post.bereich.group_type }}</b>
                                                        </div>
                                                        <div class="description">
                                                            Date Posted: <b>{{ post.date_post }}</b>
                                                        </div>
                                                        
                                                        <div class="description">
                                                            Bundesland <b>{{ post.region.bundesland }}</b>, Stadt: <b>{{ post.region.stadt }}</b>
                                                        </div>
                                                        <div class="description" style="color: red">
                                                            Score: <i><b>{{ post.score }}</b></i>
                                                        </div>
                                        


                                                    </div>
                                                </div>
                                            </div>
                                            
                                        </td>
                                    </tr>
                                </div>
                            </div>
                        </tbody>
             </table>
        </section>`,

    computed: {
        processedPosts() {
            let posts = this.results;

            // Add image_url attribute


            // Put Array into Chunks
            let i, j, chunkedArray = [], chunk = 4;
            for (i = 0, j = 0; i < posts.length; i += chunk, j++) {
                chunkedArray[j] = posts.slice(i, i + chunk);
            }
            return chunkedArray;
        },
        // showM: function() {
        //     return this.results.length === this.total_results.length && this.results.length > 0
        // }
    }
});


var vm = new Vue({
    el: '#app',
    data: function(){
        return {
            dev_project_count : 0,
            inf_project_count : 0,
            ds_project_count : 0,
            results: [],
            catdev: 50,
            catinf: cat2,
            catds: cat3,
            section1: [{name: 'Development', group: "Development", button: "btn btn-primary", width: "width:", count: 50, pix:"%"}, {name: 'Infrastructure', group: "Infrastructure", button:"btn btn-info", width: "width:", count: 30, pix:"%"}, {name: 'Data', group:"Data Science", button: "btn btn-warning", width: "width:", count: 20, pix:"%"}],
            sections: SECTIONS.split(', '), // create an array of the sections
            class_buttons1: class_buttons.split(', '),
            subDev1: subDev.split(', '),
            subInf1: subInf.split(', '),
            subDs1: subDs.split(', '),
            devSub: devWeb.split(', '),
            
            section: 'home', // set default section to 'home'
            isActive: true,
            devSub1: false,
            dev: false,
            inf: false,
            ds: false,
            selected: [],
            options: [
            { text: 'Development', value: this.subDev1 },
            { text: 'Infrastructure', value: this.subInf1 },
            { text: 'Data Science', value: this.subDs1 }
            ],
        
            styleObject: {
                color: 'red',
                font: '100px'
              },
            width1: "width: 50%",
            gg: 1,
            items: [],
            total_project_count: 0,
            total_results: [],
            loading: false,
            loading_api: false,
            group_selected: '',
            searchRoute: 'search/',
            search_term: '',
            group_clicked: true

        }
        
        


    },
    mounted() {
        this.getPosts(this.section);
        var vueInstance = this;
        var elem = document.getElementById('product-list-bottom');
        var watcher = scrollMonitor.create(elem);
        watcher.enterViewport(function() {
            console.log('hello')
            vueInstance.appendItems()
        })
        
    },
    methods: {
        appendItems: function() {
            if (this.results.length < this.total_results.length) {
                var next_data = this.total_results.slice(this.results.length, this.results.length + 10);
                this.results = this.results.concat(next_data);
            }
        },
        getPosts(section) {
            //let url = section === "home"? buildUrl(section) : buildUrl(section) + "/" + sub;
            //let url = buildUrl(section) + "/Web";
            
            let url
            if (section === "home") {
                //this.appendItems()
                url = buildUrl(section);
                console.log(url)
                this.loading = true
                
                axios.get(url).then((response) => {
                 this.group_selected = "All Projects"
                 this.total_results = response.data.project_lists
                 this.results = response.data.project_lists.slice(0, 10);
                 this.total_project_count = response.data.amount
                 console.log(this.section1[0])
                 this.section1[0].count = (100 * response.data.amount2[0])/this.total_project_count
                 this.section1[1].count = (100 * response.data.amount2[1])/this.total_project_count
                 this.loading = false

                 //if ((100 * response.data.amount2[2])/this.total_project_count) < 12) {}
                 this.section1[2].count = ((100 * response.data.amount2[2])/this.total_project_count)
                 this.section1[2].count +=5




                 console.log(this.section1[0].count)
                 console.log(this.section1[1].count)
                 console.log(this.section1[2].count)

                 //this.cat1 = (100 * this.current_project_count)/this.total_project_count
                 /*console.log(this.total_project_count)
                 console.log(this.dev_project_count)
                 console.log(this.inf_project_count)
                 console.log(this.ds_project_count)

                 console.log(this.gg)*/
                 //console.log((response.data.project_lists).length)
                 }).catch(error => { console.log(error); });
                
            }
            else if (section === "Development") {
                url = buildUrl(section);
                console.log(url)
                console.log(section)
                
                this.inf = false;
                this.ds = false;
                this.dev = true;
                axios.get(url).then((response) => {
                    this.group_selected = section
                    this.total_results = response.data.project_lists
                    this.results = response.data.project_lists.slice(0, 10);
                    this.total_project_count = response.data.amount
                    //this.results = response.data.project_lists;
                    //this.total_project_count = response.data.amount
                    // this.current_project_count = response.data.amount2[0]
                    // this.cat1 = (100 * this.current_project_count)/this.total_project_count
                    // console.log(this.total_project_count)
                    // console.log(this.current_project_count)
                    // console.log(this.cat1)
                    //console.log((response.data.project_lists).length)
                }).catch(error => { console.log(error); });
            }
            else if (section === "Infrastructure") {
               url = buildUrl(section);
               console.log(url)
               this.dev = false;
               this.ds = false;
               this.inf = true;
               axios.get(url).then((response) => {
                this.group_selected = section
                this.total_results = response.data.project_lists
                this.results = response.data.project_lists.slice(0, 10);
                this.total_project_count = response.data.amount
                //this.current_project_count = response.data.amount2[1]
                //this.cat1 = (100 * this.current_project_count)/this.total_project_count
                // console.log(this.total_project_count)
                // console.log(this.current_project_count)
                // console.log(this.gg)
                //console.log((response.data.project_lists).length)
                }).catch(error => { console.log(error); });

            }
            else if (section === "Data Science") {

               url = buildUrl(section);
               console.log(url)
               this.dev = false;
               this.inf = false;
               this.ds = true;
               axios.get(url).then((response) => {
                this.group_selected = section
                this.total_results = response.data.project_lists
                this.results = response.data.project_lists.slice(0, 10);
                this.total_project_count = response.data.amount
                // this.results = response.data.project_lists;
                // this.total_project_count = response.data.amount
                // this.current_project_count = response.data.amount2[2]
                // this.cat1 = (100 * this.current_project_count)/this.total_project_count
                // console.log(this.total_project_count)
                // console.log(this.current_project_count)
                // console.log(this.cat1)
                //console.log((response.data.project_lists).length)
            }).catch(error => { console.log(error); });
            }
            else if (section === this.search_term) {
                url = buildUrl(this.searchRoute.concat(section));
                console.log(url)
                console.log(section)
                this.inf = false;
                this.ds = false;
                this.dev = true;
                this.devSub1 = true;
                this.group_clicked =false
                axios.get(url).then((response) => {
                 this.group_selected = section
                 this.total_results = response.data.project_lists
                 this.results = response.data.project_lists.slice(0, 10);
                 this.total_project_count = response.data.amount
                 console.log(this.section1[0])
                 this.section1[0].count = (100 * response.data.amount2[0])/this.total_project_count
                 this.section1[1].count = (100 * response.data.amount2[1])/this.total_project_count
                 this.loading = false

                 //if ((100 * response.data.amount2[2])/this.total_project_count) < 12) {}
                 this.section1[2].count = ((100 * response.data.amount2[2])/this.total_project_count)
                 this.section1[2].count +=5




                 console.log(this.section1[0].count)
                 console.log(this.section1[1].count)
                 console.log(this.section1[2].count)
                    //console.log((response.data.project_lists).length)
                }).catch(error => { console.log(error); });
            }
            
        }
    },
    
});

//var myStringArray = ["Hello","World"];




/*for (var i in vm.section1){
    let dev = vm.section1[0]
    let inf = vm.section1[1]
    let ds = vm.section1[2]
    let dev_count = vm.dev_project_count
    let inf_count = vm.inf_project_count
    let ds_count = vm.ds_project_count
    Vue.set(dev, 'count', dev_count)
    Vue.set(inf, 'count', inf_count)
    Vue.set(ds, 'count', ds_count)
    
    console.log(vm.dev_project_count)
}*/


