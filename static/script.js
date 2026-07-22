document.addEventListener("DOMContentLoaded", function () {

    // ======================
    // Search
    // ======================

    const search = document.getElementById("searchInput");

    if(search){

        search.addEventListener("keyup", function(){

            let value=this.value.toLowerCase();

            let rows=document.querySelectorAll("#taskTable tbody tr");

            rows.forEach(function(row){

                row.style.display=row.innerText.toLowerCase().includes(value)
                ? ""
                : "none";

            });

        });

    }

    // ======================
    // Filter
    // ======================

    document.querySelectorAll(".filter-btn").forEach(button=>{

        button.addEventListener("click",function(){

            let filter=this.dataset.filter;

            let rows=document.querySelectorAll("#taskTable tbody tr");

            rows.forEach(function(row){

                if(filter=="all"){

                    row.style.display="";

                }

                else{

                    row.style.display=row.innerText.includes(filter)
                    ? ""
                    : "none";

                }

            });

        });

    });

    // ======================
    // Dark Mode
    // ======================

    const btn=document.getElementById("darkModeBtn");

    if(btn){

        btn.addEventListener("click",function(){

            document.body.classList.toggle("dark-mode");

            if(document.body.classList.contains("dark-mode")){

                btn.innerHTML="☀ Light Mode";

            }

            else{

                btn.innerHTML="🌙 Dark Mode";

            }

        });

    }

});
