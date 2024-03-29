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
const subInf = "ERP, Admin";
const subDs = "Big Data, Business Intelligence, Machine Learning";
const devWeb = "Fullstack, Backend, Frontend"
const class_buttons = "btn btn-primary, btn btn-info, btn btn-warning"


    //let url = section === "home"? buildUrl(section) : buildUrl(section) + "/" + sub;
    //let url = buildUrl(section) + "/Web";



//var country_selected = document.getElementById("Sub");

const BaseUrl = "http://127.0.0.1:5000/";
const searchBaseUrl = "http://127.0.0.1:5000/search/";
const queryBaseUrl = "http://127.0.0.1:5000/query";
//const url1 = `${queryBaseUrl}&search_term=${searchTerm}`;


function buildUrl(url) {

    return BaseUrl + url
}

function searchUrl(url) {

    return searchBaseUrl + url
}
function queryUrl(searchTerm) {

    return `${queryBaseUrl}${'?'}search=${searchTerm}`;
}
function buildSecUrl(url, sub) {

    return BaseUrl + url + '/' + sub
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

                                                            Sub-Category: <b>{{ post.bereich.group_type }}</b>, Stack: <b>{{ post.bereich.group_type_stack }}</b>
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

            results: [],
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
            items: [],
            total_project_count: 0,
            total_results: [],
            loading: false,
            loading_api: false,
            group_selected: '',
            searchRoute: 'search/',
            search_term: '',
            group_clicked: true,
            queryRoute: '?search=',
            selected: '',
            selected_dv: '',
            selected_inf: '',
            selected_ds: '',
            options: [
                { text: 'One', value: 'A' },
                { text: 'Two', value: 'B' },
                { text: 'Three', value: 'C' }
              ],
            group_selected: '',
            folders: [
                {name: 'Development', pages: [{name: 'Web', sub1: [{name: 'Backend'}, {name: 'Frontend'}, {name: 'Fullstack'}] }, {name: 'Mobile', sub1: [{name: 'Native'}, {name: 'Cross-Platform'}]}] },
                {name: 'Infrastructure', pages: [{name: 'ERP', sub1: [{name: 'SAP'}]}, {name: 'Admin', sub1: [{name: 'Microsoft'}]}, {name: 'Others', sub1: [{name: 'Other'}]}] },
                {name: 'Data Science', pages: [{name: 'Big Data', sub1: []}, {name: 'Business Intelligence', sub1: []}, {name: 'Machine Learning', sub1: []}] },
            ],
            expanded: false,


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
        print: function(name) {
            console.log(name)
        },


        toggle: function (idname) {
            if(document.getElementById(idname).style.display == "none"){
                document.getElementById(idname).style.display = "inline";


            }
            else if(document.getElementById(idname).style.display == "inline") {
                document.getElementById(idname).style.display = "none";

            }

          },


        appendItems: function() {
            if (this.results.length < this.total_results.length) {
                var next_data = this.total_results.slice(this.results.length, this.results.length + 10);
                this.results = this.results.concat(next_data);
            }
        },
        dropdown: function(a) {
            console.log(a)
        },
        fetchData() {
          axios.get('https://api.coinmarketcap.com/v1/ticker/'+this.$route.params.id+'/')
          .then((resp) => {
            this.coin = resp.data[0]
            console.log(resp)
          })
          .catch((err) => {
            console.log(err)
          })
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
                 this.section1[2].count = ((100 * response.data.amount2[2])/this.total_project_count) + 5
                 //this.section1[2].count +=5




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
                this.group_selected = ''
                this.group_selected = section;
                console.log(this.group_selected)

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
               console.log(section)
               this.group_selected = ''
               this.group_selected = section;
               console.log(this.group_selected)
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
               console.log(section)
               this.group_selected = ''
               this.group_selected = section;
               console.log(this.group_selected)
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
                //url = buildUrl(this.searchRoute.concat(section));
                url = queryUrl(section);
                console.log(url)
                console.log(section)


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
            else if (section === this.selected_dv) {
                //let category_selected = this.group_selected
                //url = buildUrl(this.searchRoute.concat(section));
                url = buildSecUrl("Development", section);

                console.log(url)
                console.log(section)


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
            else if (section === this.selected_inf) {
                //let category_selected = this.group_selected
                //url = buildUrl(this.searchRoute.concat(section));
                url = buildSecUrl("Infrastructure", section);

                console.log(url)
                console.log(section)


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
            else if (section === this.selected_ds) {
                //let category_selected = this.group_selected
                //url = buildUrl(this.searchRoute.concat(section));
                url = buildSecUrl("Data Science", section);


                console.log(url)
                console.log(section)


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
            else {
                //let category_selected = this.group_selected
                //url = buildUrl(this.searchRoute.concat(section));
                url = buildUrl(section);


                console.log(url)
                console.log(section)


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
    watch: {
      selected_dv: function() {
        console.log(this.selected_dv)
        this.getPosts(this.selected_dv)

      },
      selected_inf: function() {
        console.log(this.selected_inf)
        this.getPosts(this.selected_inf)
      },
      selected_ds: function() {
        console.log(this.selected_ds)
        this.getPosts(this.selected_ds)
      }
    }

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
