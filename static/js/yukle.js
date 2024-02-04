var titles = ['Büyük dosyaların yüklenmesi uzun sürer.', 'Bu bir yapay zekadır. Sonuçlar mükemmel değildir.', 'Bulanık resimlerde performans düşer.' ,'by Alper Tuna KILIÇ.'];
var currentIndex = 0;
var loading = ['Yükleniyor.', 'Yükleniyor..', 'Yükleniyor...', 'Yükleniyor....', 'Yükleniyor.....'];
var currentIndex2 = 0;
var waits = ['Resminiz yüklenirken sabırlı olun.', 'Resminiz yüklenirken sabırlı olun..', 'Resminiz yüklenirken sabırlı olun...','Resminiz yüklenirken sabırlı olun....','Resminiz yüklenirken sabırlı olun.....']
var currentIndex3 = 0;

function changeLoading() {
    load1 = document.getElementById('alter_title').textContent = titles[currentIndex];
    currentIndex = (currentIndex + 1) % titles.length;
    setTimeout(changeLoading, 3000);
}

function changeTitle() {
    load = document.getElementById('load').textContent = loading[currentIndex2];
    currentIndex2 = (currentIndex2 + 1) % loading.length;
    setTimeout(changeTitle, 500);
    
}


function hideAlt() {
    wait = document.getElementById('alter_title1').textContent = waits[currentIndex3];
    currentIndex3 = (currentIndex3 +1) % waits.length;
    setTimeout(hideAlt, 500)
}