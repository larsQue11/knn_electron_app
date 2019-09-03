function sendToPython() {

    // Use python shell
    let {PythonShell} = require('python-shell');

    var options = {
        mode: 'text',
        // pythonPath: '../venv/bin/python',
        pythonPath: './venv/bin/python',
        // args: ['sepal_length','sepal_width','petal_length','petal_width']
        args: [sepal_length,sepal_width,petal_length,petal_width]
    }

    PythonShell.run('./backend/knn_iris.py',options,function(err,results) {
        if (err) throw err;
        console.log(results)
        //Do things with the returned results from knn_iris.py here:
    })
}

function get_data() {

    const status = "get_data/iris.js called"
    console.log(status)

    if (sepal_length = document.getElementById("sepal_length").value.length > 0) {
        var sepal_length = document.getElementById("sepal_length").value
    } else { var sepal_length = -1 }
    
    if (document.getElementById("sepal_width").value.length > 0) {
        var sepal_width = document.getElementById("sepal_width").value
    } else { var sepal_width = -1 }

    if (document.getElementById("petal_length").value.length > 0) {
        var petal_length = document.getElementById("petal_length").value
    } else { var petal_length = -1 }
    
    if (document.getElementById("petal_width").value.length > 0) {
        var petal_width = document.getElementById("petal_width").value
    } else { var petal_width = -1 }

    var results = [sepal_length, sepal_width, petal_length, petal_width]
    console.log("Retrieved data from HTML: " + results)

    sendToPython()
}

function clear_data() {

    console.log('clear_data called')
    document.getElementById("sepal_length").value = ""
    document.getElementById("sepal_width").value = ""
    document.getElementById("petal_length").value = ""
    document.getElementById("petal_width").value = ""
}