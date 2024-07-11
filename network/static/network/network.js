document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("Postbtn").addEventListener("click", function () {
        post();
    });

    loadPosts()
});


function loadPosts() {

    const posts = document.querySelectorAll("#posts");
    if(posts){
        posts.forEach(post => {
            post.remove();
        });
    }

    fetch("/posts")
        .then(response => response.json())
        .then(result => {
            result.forEach(post => {
                createPost(post);
            });
        });

}


function createPost(post) {
    const indexpage = document.querySelector("#index-page");
    const userInfoDiv = document.getElementById('user-info');
    const username = userInfoDiv.getAttribute('data-username');

    const div = document.createElement("div");
    div.id = "posts";
    div.className = "row border border-secondary mb-2 rounded";

    const namediv = document.createElement("div");
    namediv.className = "col";
    const name = document.createElement("p");
    name.className = "fs-3 fw-bold text-secondary";
    name.innerText = post.account;
    namediv.appendChild(name);

    const breakdiv = document.createElement("div");
    breakdiv.className = "w-100";

    const postdiv = document.createElement("div");
    postdiv.className = "col";
    
    const edit = document.createElement("a")
    edit.className = "fs-6 fw-bold text-decoration-none";
    edit.href = "#";
    edit.innerText = "Edit";
    
    const content = document.createElement("p");
    content.className = "fs-6 fw-thin  p-0 m-0";
    content.innerText = post.content;
    
    const timestamp = document.createElement("p");
    timestamp.className = "fs-6 fw-thin text-muted";
    timestamp.innerText = post.timestamp;
    
    const likebtn = document.createElement("button");
        
        likebtn.className = post.likes.includes(username) ? "btn btn-dark":"btn btn-outline-dark";
        likebtn.addEventListener("click", () => {
            togglelike(post, likebtn, username);
        });    
    likebtn.innerHTML = `&#9825; ${post.likes.length}`
    
    postdiv.appendChild(edit);
    postdiv.appendChild(content);
    postdiv.appendChild(likebtn);
    postdiv.appendChild(timestamp);

    const breakdiv2 = document.createElement("div");
    breakdiv2.className = "w-100";
    const btndiv = document.createElement("div");
    btndiv.className = "col";

    

    div.appendChild(namediv);
    div.appendChild(breakdiv);
    div.appendChild(postdiv);
    div.appendChild(breakdiv2);
    div.appendChild(btndiv);

    indexpage.appendChild(div);

}


function post() {
    content = document.querySelector("#content").value;
    document.querySelector("#content").value = "";
    fetch("/upload", {
        method: "POST",
        body: JSON.stringify({
            content: content
        })
    })
        .then(response => response.json())
        .then(result => {
            if (result.status !== 201) {
                error = result.error;
                if (document.querySelector("#error-div") === null){
                    const col = document.createElement("div");
                    col.className = "col order-1";
                    col.id = "error-div";
                    const div = document.createElement("div");
                    div.className = "alert alert-danger";
                    div.role = "alert";
                    div.innerHTML = error;
                    const breakdiv = document.createElement("div");
                    breakdiv.className = "w-100 order-2";
                    col.appendChild(div)
                    document.querySelector("#Create-Post-div").appendChild(col);
                    document.querySelector("#Create-Post-div").appendChild(breakdiv);
                    setTimeout(()=>{
                        breakdiv.remove();
                        col.remove();
                    },5000);
                }
            }else{
                if (document.querySelector("#success-div") === null){
                    message = result.message;
                    const col = document.createElement("div");
                    col.className = "col order-1";
                    col.id = "success-div";
                    const div = document.createElement("div");
                    div.className = "alert alert-success";
                    div.role = "alert";
                    div.innerHTML = message;
                    const breakdiv = document.createElement("div");
                    breakdiv.className = "w-100 order-2";
                    col.appendChild(div)
                    document.querySelector("#Create-Post-div").appendChild(col);
                    document.querySelector("#Create-Post-div").appendChild(breakdiv);
                    setTimeout(()=>{
                        breakdiv.remove();
                        col.remove();
                    },5000);
                }
            }

            loadPosts();
        });
}


function togglelike(post,likebtn,username)
{
    action = post.likes.includes(username) ? "unlike" : "like";
    fetch(`/${action}`,{
        method: "POST",
        body: JSON.stringify({
            id: post.id
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 201) {
            if (action === "like") {
                post.likes.push(username);
                likebtn.className = "btn btn-dark";
            } else {
                post.likes = post.likes.filter(user => user !== username);
                likebtn.className = "btn btn-outline-dark";
            }
            likebtn.innerHTML = `&#9825; ${post.likes.length}`;
        }
    });
}
