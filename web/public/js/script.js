(() => {
    let elements = document.querySelectorAll("#tarih");
    elements.forEach((element) => {
        let date = new Date(element.innerText);
        element.innerText = date.toLocaleDateString("tr-TR", {
            day: "numeric",
            month: "long",
            weekday: "long",
        });           
    });
})();
