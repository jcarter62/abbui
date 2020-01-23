// // Change state of favorite indicator.
// function fav_click(id) {
//     let elem = document.getElementById(id);
//     if (elem.classList.contains('fav-dim')) {
//         elem.classList.remove('fav-dim')
//     } else {
//         elem.classList.add('fav-dim')
//     }
// }

class Favorites {

    fav_toggle_btn = 'favorite-toggle';
    dim_class = 'fav-dim';

    constructor() {
        if (typeof (Storage) !== 'undefined') {
            this.localstore = true;
        } else {
            this.localstore = false;
        }
    }

    fav_click(id) {
        let elem = document.getElementById(id);
        if (elem.classList.contains(this.dim_class)) {
            elem.classList.remove(this.dim_class)
            this.set(id)
        } else {
            elem.classList.add(this.dim_class)
            this.del(id)
        }
    }

    get(id) {
        if (this.localstore) {
            let val = localStorage[id]
            if (val == null) {
                val = '0';
            }
            return val;
        } else {
            return false;
        }
    }

    set(id) {
        if (this.localstore) {
            localStorage[id] = '1';
        }
    }

    del(id) {
        if (this.localstore) {
            localStorage.removeItem(id);
        }
    }

    // load all favorites, and set appropriate dim class for each
    // value found in local storage.
    load_favorites() {
        let elems = document.getElementsByClassName('favorite');
        for (let i in elems) {
            let e = elems[i];
            if (typeof (e) !== 'object') {

            } else {
                let id = e['id'];
                if (this.get(id) == '1') {
                    e.classList.remove(this.dim_class)
                } else {
                    try {
                        e.classList.add(this.dim_class)
                    } catch (err) {
                        console.log(err.message);
                    }
                }
            }
        }
        // Now restore button at top of table.
        if ( this.get(this.fav_toggle_btn) == '1' ) {
            let element = document.getElementById(this.fav_toggle_btn);
            if ( element != null ) {
                element.classList.remove(this.dim_class);
                this.show_only_favorites()
            }
        }
    }

    show_only_favorites() {
        let elements = document.getElementsByClassName('datarow');
        for (let i in elements) {
            let e = elements[i];
            if (typeof (e) !== 'object') {

            } else {
                let id = e['id'] + 'X';
                if (this.get(id) == '1') {
                    e.classList.remove('hide-row')
                } else {
                    try {
                        e.classList.add('hide-row')
                    } catch (err) {
                        console.log(err.message);
                    }
                }
            }
        }
    }

    show_all() {
        let elements = document.getElementsByClassName('datarow');
        for (let i in elements) {
            let e = elements[i];
            if (typeof (e) !== 'object') {
                //
            } else {
                e.classList.remove('hide-row')
            }
        }
    }


    toggle() {
        let element = document.getElementById(this.fav_toggle_btn)
        try {
            let isDim = element.classList.contains(this.dim_class);
            if ( isDim ) {
                element.classList.remove(this.dim_class);
                this.show_only_favorites();
                this.set(this.fav_toggle_btn)
            } else {
                element.classList.add(this.dim_class);
                this.show_all();
                this.del(this.fav_toggle_btn)
            }
        } catch (e) {
            console.log(e.message);
        }
    }
}

