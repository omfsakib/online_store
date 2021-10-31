function categoryFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('categoryInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("id_category");
    li = ul.getElementsByTagName('li');
  
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("label")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }

  
  function tagFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('tagInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("id_tags");
    li = ul.getElementsByTagName('li');
  
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("label")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }


  function productFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('liveInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("product_name");
    li = ul.getElementsByClassName('col-lg-3');
  
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("strong")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }