"use strict";
function _typeof(e) {
    return (_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
        return typeof e
    }
        : function (e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        }
    )(e)
}
function ownKeys(t, e) {
    var r, n = Object.keys(t);
    return Object.getOwnPropertySymbols && (r = Object.getOwnPropertySymbols(t),
        e && (r = r.filter(function (e) {
            return Object.getOwnPropertyDescriptor(t, e).enumerable
        })),
        n.push.apply(n, r)),
        n
}
function _objectSpread(t) {
    for (var e = 1; e < arguments.length; e++) {
        var r = null != arguments[e] ? arguments[e] : {};
        e % 2 ? ownKeys(Object(r), !0).forEach(function (e) {
            _defineProperty(t, e, r[e])
        }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : ownKeys(Object(r)).forEach(function (e) {
            Object.defineProperty(t, e, Object.getOwnPropertyDescriptor(r, e))
        })
    }
    return t
}
function _defineProperty(e, t, r) {
    return (t = _toPropertyKey(t)) in e ? Object.defineProperty(e, t, {
        value: r,
        enumerable: !0,
        configurable: !0,
        writable: !0
    }) : e[t] = r,
        e
}
function _toPropertyKey(e) {
    e = _toPrimitive(e, "string");
    return "symbol" == _typeof(e) ? e : String(e)
}
function _toPrimitive(e, t) {
    if ("object" != _typeof(e) || !e)
        return e;
    var r = e[Symbol.toPrimitive];
    if (void 0 === r)
        return ("string" === t ? String : Number)(e);
    r = r.call(e, t || "default");
    if ("object" != _typeof(r))
        return r;
    throw new TypeError("@@toPrimitive must return a primitive value.")
}
function _slicedToArray(e, t) {
    return _arrayWithHoles(e) || _iterableToArrayLimit(e, t) || _unsupportedIterableToArray(e, t) || _nonIterableRest()
}
function _nonIterableRest() {
    throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
}
function _unsupportedIterableToArray(e, t) {
    var r;
    if (e)
        return "string" == typeof e ? _arrayLikeToArray(e, t) : "Map" === (r = "Object" === (r = Object.prototype.toString.call(e).slice(8, -1)) && e.constructor ? e.constructor.name : r) || "Set" === r ? Array.from(e) : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? _arrayLikeToArray(e, t) : void 0
}
function _arrayLikeToArray(e, t) {
    (null == t || t > e.length) && (t = e.length);
    for (var r = 0, n = new Array(t); r < t; r++)
        n[r] = e[r];
    return n
}
function _iterableToArrayLimit(e, t) {
    var r = null == e ? null : "undefined" != typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
    if (null != r) {
        var n, o, i, a, s = [], d = !0, l = !1;
        try {
            if (i = (r = r.call(e)).next,
                0 === t) {
                if (Object(r) !== r)
                    return;
                d = !1
            } else
                for (; !(d = (n = i.call(r)).done) && (s.push(n.value),
                    s.length !== t); d = !0)
                    ;
        } catch (e) {
            l = !0,
                o = e
        } finally {
            try {
                if (!d && null != r.return && (a = r.return(),
                    Object(a) !== a))
                    return
            } finally {
                if (l)
                    throw o
            }
        }
        return s
    }
}
function _arrayWithHoles(e) {
    if (Array.isArray(e))
        return e
}
function sendEmailAjax(e) {
    e.preventDefault();
    var o = e.currentTarget
        , e = o.querySelector('[name="newnumber"]').value;
    if (!e) {
        o.querySelectorAll(".error-message").forEach(function (e) {
            return e.remove()
        }),
            o.querySelectorAll("label.not-valid").forEach(function (e) {
                return e.classList.remove("not-valid")
            });
        for (var e = Object.fromEntries(new FormData(o)), t = {}, r = {}, n = 0, i = Object.entries(e); n < i.length; n++) {
            var a, s = _slicedToArray(i[n], 2), d = s[0], s = s[1];
            ["company", "email", "message", "name", "newnumber", "policy", "subject", "tel"].includes(d) ? t[d] = s : (a = (a = o.querySelector('[name="'.concat(d, '"]'))) ? a.placeholder : d,
                r[d] = {
                    value: s,
                    label: a
                })
        }
        e = _objectSpread(_objectSpread({}, t), {}, {
            extra_fields: r
        });
        fetch("/send-email", {
            method: "POST",
            body: JSON.stringify(e),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function (t) {
            return 429 === t.status ? {
                ok: !1,
                status: 429,
                body: null
            } : t.ok ? "0" === t.headers.get("Content-Length") ? {
                ok: !0,
                status: t.status,
                body: {}
            } : t.json().then(function (e) {
                return {
                    ok: t.ok,
                    status: t.status,
                    body: e
                }
            }) : t.json().then(function (e) {
                return {
                    ok: !1,
                    status: t.status,
                    body: e
                }
            })
        }).then(function (e) {
            var t = e.ok
                , r = e.status
                , n = e.body;
            t ? o.querySelector(".form-message__text").textContent = translation.formSent : (o.querySelector(".form-message__text").textContent = "",
                429 === r ? ((e = document.createElement("p")).textContent = translation.errors.tooManyRequests || "Too many requests. Please try again later.",
                    e.className = "error-message",
                    o.querySelector(".form-message__text").appendChild(e)) : (Object.keys(n).forEach(function (e) {
                        var t = o.querySelector('[name="'.concat(e, '"]'))
                            , r = t.closest("label")
                            , r = (r && r.classList.add("not-valid"),
                                document.createElement("p"));
                        r.textContent = n[e].map(function (e) {
                            return translation.errors[e] || e
                        }).join(", "),
                            r.className = "error-message",
                            t.insertAdjacentElement("afterend", r)
                    }),
                        o.querySelector(".error-message") && o.querySelectorAll(".error-message").forEach(function (e, t) {
                            0 !== t && e.remove()
                        })))
        }).catch(function (e) {
            console.error("Error:", e);
            e = document.createElement("p");
            e.textContent = translation.errors.errorDefault || "An error occurred. Please try again later.",
                e.className = "error-message",
                o.querySelector(".form-message__text").appendChild(e)
        })
    }
}
function _toConsumableArray(e) {
    return _arrayWithoutHoles(e) || _iterableToArray(e) || _unsupportedIterableToArray(e) || _nonIterableSpread()
}
function _nonIterableSpread() {
    throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
}
function _unsupportedIterableToArray(e, t) {
    var r;
    if (e)
        return "string" == typeof e ? _arrayLikeToArray(e, t) : "Map" === (r = "Object" === (r = Object.prototype.toString.call(e).slice(8, -1)) && e.constructor ? e.constructor.name : r) || "Set" === r ? Array.from(e) : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? _arrayLikeToArray(e, t) : void 0
}
function _iterableToArray(e) {
    if ("undefined" != typeof Symbol && null != e[Symbol.iterator] || null != e["@@iterator"])
        return Array.from(e)
}
function _arrayWithoutHoles(e) {
    if (Array.isArray(e))
        return _arrayLikeToArray(e)
}
function _arrayLikeToArray(e, t) {
    (null == t || t > e.length) && (t = e.length);
    for (var r = 0, n = new Array(t); r < t; r++)
        n[r] = e[r];
    return n
}
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".email-form").forEach(function (e) {
        e.addEventListener("submit", sendEmailAjax)
    })
}),
    document.addEventListener("DOMContentLoaded", function () {
        var r, e = [].slice.call(document.querySelectorAll(".lazy-background"));
        "IntersectionObserver" in window && (r = new IntersectionObserver(function (e, t) {
            e.forEach(function (e) {
                var t;
                e.isIntersecting && (t = e.target.getAttribute("data-bg"),
                    e.target.style.backgroundImage = "url('" + t + "')",
                    e.target.classList.add("visible"),
                    r.unobserve(e.target))
            })
        }
        ),
            e.forEach(function (e) {
                r.observe(e)
            }))
    }),
    document.getElementById("cookie-banner") && (setCookie = function (e, t, r) {
        var n = new Date
            , r = (n.setTime(n.getTime() + 24 * r * 60 * 60 * 1e3),
                "expires=" + n.toUTCString());
        document.cookie = e + "=" + t + ";" + r + ";path=/"
    }
        ,
        getCookie = function (e) {
            e = ("; " + document.cookie).split("; " + e + "=");
            if (2 == e.length)
                return e.pop().split(";").shift()
        }
        ,
        acceptCookies = function () {
            setCookie("cookiesAccepted", "yes", 365),
                document.getElementById("cookie-banner").style.display = "none",
                "function" == typeof gtag && gtag("consent", "update", {
                    ad_storage: "granted",
                    analytics_storage: "granted",
                    ad_user_data: "granted",
                    ad_personalization: "granted"
                })
        }
        ,
        cookieBannerDisplayed = !(rejectCookies = function () {
            setCookie("cookiesAccepted", "no", 365),
                document.getElementById("cookie-banner").style.display = "none",
                "function" == typeof gtag && gtag("consent", "update", {
                    ad_storage: "denied",
                    analytics_storage: "denied",
                    ad_user_data: "denied",
                    ad_personalization: "denied"
                })
        }
        ),
        window.addEventListener("scroll", function () {
            var e = window.scrollY || document.documentElement.scrollTop
                , t = getCookie("cookiesAccepted");
            100 < e && !cookieBannerDisplayed && !t && (document.getElementById("cookie-banner").style.display = "flex",
                cookieBannerDisplayed = !0)
        }),
        window.onload = function () {
            var e = getCookie("cookiesAccepted");
            e ? "yes" === e ? gtag("consent", "update", {
                ad_storage: "granted",
                analytics_storage: "granted",
                ad_user_data: "granted",
                ad_personalization: "granted"
            }) : "no" === e && gtag("consent", "update", {
                ad_storage: "denied",
                analytics_storage: "denied",
                ad_user_data: "denied",
                ad_personalization: "denied"
            }) : document.getElementById("cookie-banner").style.display = "flex"
        }
    );
    var setCookie, getCookie, acceptCookies, rejectCookies, cookieBannerDisplayed, 
    menuBtn = document.querySelector(".header__ham"), 
    mainMenu = document.querySelector(".header__menu"), 
    header = document.querySelector(".header"),
    appContainer = (
        menuBtn.addEventListener("click", function () {
            menuBtn.classList.toggle("open"),
                mainMenu.classList.toggle("open"),
                header.classList.toggle("open")
        }),

        window.onscroll = function () {
            stickyHeader()
        }
        ,
        document.querySelector(".app-container")), sticky = header.offsetTop + 51;
function stickyHeader() {
    window.pageYOffset > sticky ? (header.classList.add("sticky"),
        appContainer.classList.add("sticky")) : (header.classList.remove("sticky"),
            appContainer.classList.remove("sticky"))
}
function toggleActiveClass(e) {
    var t = e.parentElement;
    t.classList.toggle("checked"),
        t.classList.contains("checked") ? e.checked = !0 : e.checked = !1
}
function toggleClass(e) {
    e.classList.toggle("active")
}
var allMenuWithSubmenu = document.querySelectorAll(".header__menu-list li.has-children");
function addToggleClassToParent(e) {
    e.classList.toggle("open")
}
function addSquareClassToImages() {
    var e = document.querySelectorAll(".header__logo img")
        , t = document.querySelectorAll(".footer__logo img");
    [].concat(_toConsumableArray(e), _toConsumableArray(t)).forEach(function (r) {
        r.onload = function () {
            var e = r.naturalWidth
                , t = r.naturalHeight;
            Math.abs(e / t - 1) <= .1 && (r.classList.add("square"),
                r.closest(".header__logo") ? r.closest(".header").classList.add("square") : r.closest(".footer__logo") && r.closest(".footer").classList.add("square"))
        }
            ,
            r.complete && r.onload()
    })
}
allMenuWithSubmenu && allMenuWithSubmenu.forEach(function (t) {
    t.addEventListener("click", function () {
        t.classList.toggle("open")
    }),
        document.addEventListener("click", function (e) {
            t.contains(e.target) || t.classList.remove("open")
        })
}),
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".header__logo span").forEach(function (e) {
            var t, r = e.innerHTML.trim();
            r && (t = r[0],
                r = r.slice(1),
                " " !== t) && (t = "<span>".concat(t, "</span>").concat(r),
                    e.innerHTML = t)
        })
    }),
    document.addEventListener("DOMContentLoaded", addSquareClassToImages);
var handleSwipe, showSlide, slides, dotsContainer, prevArrow, nextArrow, dots, currentSlide, touchStartX, touchEndX, addSlideAnimation, removeSlideAnimation, updateSlider, handleTouchStart, handleTouchMove, handleTouchEnd, checkScreenWidth, sliderItems, prevButton, nextButton, sliderNumbers, _currentSlide, startX, endX, totalSlides, updateSliderNumbers, moveSlider, handleSwipeGesture, sliderItemsEl, prevArrowBtnEl, nextArrowBtnEl, sliderNumbersEl, slideWidth, visibleSlidesCount, slideMargin, currentSlideIndex, _touchStartX, _touchEndX, itemsNdRev, prevButtonNdRev, nextButtonNdRev, currentScrollNdRev, startXNdRev, firstItemNdRev, itemMarginRightNdRev, scrollStepNdRev, slider = document.querySelector(".main-slider__items"), sliderContainer = (slider && (handleSwipe = function () {
    100 < touchStartX - touchEndX ? currentSlide = (currentSlide + 1) % slides.length : 100 < touchEndX - touchStartX && (currentSlide = (currentSlide - 1 + slides.length) % slides.length),
        showSlide(currentSlide)
}
    ,
    showSlide = function (e) {
        dots.forEach(function (e) {
            e.classList.remove("active")
        }),
            dots[e].classList.add("active");
        var t = slides[0].offsetWidth;
        slider.style.transform = "translateX(-".concat(e * t, "px)"),
            currentSlide = e
    }
    ,
    slides = document.querySelectorAll(".main-slider__item"),
    dotsContainer = document.querySelector(".main-slider__dots"),
    prevArrow = document.querySelector(".main-slider__arrow.prev"),
    nextArrow = document.querySelector(".main-slider__arrow.next"),
    dots = [],
    slides.forEach(function () {
        var e = document.createElement("span");
        e.classList.add("main-slider__dot"),
            dotsContainer.appendChild(e),
            dots.push(e)
    }),
    showSlide(currentSlide = 0),
    touchEndX = touchStartX = 0,
    slider.addEventListener("touchstart", function (e) {
        touchStartX = e.touches[0].clientX
    }),
    slider.addEventListener("touchend", function (e) {
        touchEndX = e.changedTouches[0].clientX,
            handleSwipe()
    }),
    slider.addEventListener("mousedown", function (e) {
        touchStartX = e.clientX
    }),
    slider.addEventListener("mouseup", function (e) {
        touchEndX = e.clientX,
            handleSwipe()
    }),
    prevArrow.addEventListener("click", function () {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length,
            showSlide(currentSlide)
    }),
    nextArrow.addEventListener("click", function () {
        currentSlide = (currentSlide + 1) % slides.length,
            showSlide(currentSlide)
    }),
    dots.forEach(function (e, t) {
        e.addEventListener("click", function () {
            showSlide(t)
        })
    })),
    document.querySelector(".reviews-slider__container")), sliderContainerEl = (sliderContainer && (addSlideAnimation = function () {
        sliderItems[_currentSlide].classList.add("slide-in-right")
    }
        ,
        removeSlideAnimation = function () {
            sliderItems.forEach(function (e) {
                e.classList.remove("slide-in-right")
            })
        }
        ,
        updateSlider = function () {
            sliderItems.forEach(function (e) {
                e.style.display = "none"
            }),
                sliderItems[_currentSlide].style.display = "block",
                sliderNumbers.textContent = "".concat(_currentSlide + 1, "/").concat(totalSlides),
                addSlideAnimation()
        }
        ,
        handleTouchStart = function (e) {
            startX = e.touches[0].pageX
        }
        ,
        handleTouchMove = function (e) {
            endX = e.touches[0].pageX
        }
        ,
        handleTouchEnd = function () {
            var e = endX - startX;
            Math.abs(e) < 10 || (50 < e ? --_currentSlide < 0 && (_currentSlide = totalSlides - 1) : e < -50 && totalSlides <= ++_currentSlide && (_currentSlide = 0),
                updateSlider())
        }
        ,
        checkScreenWidth = function () {
            window.innerWidth <= 768 ? (sliderContainer.addEventListener("touchstart", handleTouchStart),
                sliderContainer.addEventListener("touchmove", handleTouchMove),
                sliderContainer.addEventListener("touchend", handleTouchEnd)) : (sliderContainer.removeEventListener("touchstart", handleTouchStart),
                    sliderContainer.removeEventListener("touchmove", handleTouchMove),
                    sliderContainer.removeEventListener("touchend", handleTouchEnd))
        }
        ,
        sliderItems = document.querySelectorAll(".reviews-slider__item"),
        prevButton = document.querySelector(".reviews-slider__arrow.prev"),
        nextButton = document.querySelector(".reviews-slider__arrow.next"),
        sliderNumbers = document.querySelector(".reviews-slider__numbers"),
        endX = startX = _currentSlide = 0,
        totalSlides = sliderItems.length,
        prevButton.addEventListener("click", function () {
            --_currentSlide < 0 && (_currentSlide = totalSlides - 1),
                removeSlideAnimation(),
                updateSlider()
        }),
        nextButton.addEventListener("click", function () {
            totalSlides <= ++_currentSlide && (_currentSlide = 0),
                removeSlideAnimation(),
                updateSlider()
        }),
        sliderContainer.addEventListener("touchstart", handleTouchStart),
        sliderContainer.addEventListener("touchmove", handleTouchMove),
        sliderContainer.addEventListener("touchend", handleTouchEnd),
        checkScreenWidth(),
        updateSlider(),
        window.addEventListener("resize", checkScreenWidth)),
        document.querySelector(".front-blog.slider .front-blog__items")), translations = (sliderContainerEl && (updateSliderNumbers = function () {
            var e = sliderItemsEl.length;
            sliderNumbersEl.textContent = "".concat(currentSlideIndex + 1, "/").concat(e)
        }
            ,
            moveSlider = function (e) {
                var t = sliderItemsEl.length - 1
                    , e = ("prev" === e && 0 < currentSlideIndex ? currentSlideIndex-- : "next" === e && currentSlideIndex < t && currentSlideIndex++,
                        -(slideWidth + slideMargin) * currentSlideIndex);
                sliderContainerEl.style.transform = "translateX(".concat(e, "px)"),
                    updateSliderNumbers()
            }
            ,
            handleSwipeGesture = function () {
                var e = _touchEndX - _touchStartX;
                0 < e && slideWidth / 2 < e ? moveSlider("prev") : e < 0 && Math.abs(e) > slideWidth / 2 && moveSlider("next")
            }
            ,
            sliderItemsEl = document.querySelectorAll(".front-blog.slider .front-blog__item"),
            prevArrowBtnEl = document.querySelector(".front-blog.slider .front-blog__arrow.prev"),
            nextArrowBtnEl = document.querySelector(".front-blog.slider .front-blog__arrow.next"),
            sliderNumbersEl = document.querySelector(".front-blog.slider .front-blog__numbers"),
            slideWidth = sliderItemsEl[0].offsetWidth,
            visibleSlidesCount = 2,
            slideMargin = 16,
            _touchEndX = _touchStartX = currentSlideIndex = 0,
            prevArrowBtnEl.addEventListener("click", function () {
                moveSlider("prev")
            }),
            nextArrowBtnEl.addEventListener("click", function () {
                moveSlider("next")
            }),
            sliderContainerEl.addEventListener("touchstart", function (e) {
                _touchStartX = e.touches[0].clientX
            }),
            sliderContainerEl.addEventListener("touchend", function (e) {
                _touchEndX = e.changedTouches[0].clientX,
                    handleSwipeGesture()
            }),
            sliderContainerEl.addEventListener("mousedown", function (e) {
                _touchStartX = e.clientX
            }),
            sliderContainerEl.addEventListener("mouseup", function (e) {
                _touchEndX = e.clientX,
                    handleSwipeGesture()
            }),
            updateSliderNumbers(),
            itemsNdRev = document.querySelector(".reviews-slider-three__items")) && (prevButtonNdRev = document.querySelector(".reviews-slider-three__arrow.prev"),
                nextButtonNdRev = document.querySelector(".reviews-slider-three__arrow.next"),
                currentScrollNdRev = 0,
                firstItemNdRev = itemsNdRev.firstElementChild,
                itemMarginRightNdRev = parseFloat(window.getComputedStyle(firstItemNdRev).getPropertyValue("margin-right")),
                scrollStepNdRev = firstItemNdRev.getBoundingClientRect().width + itemMarginRightNdRev,
                prevButtonNdRev.addEventListener("click", function () {
                    currentScrollNdRev = Math.max(currentScrollNdRev - scrollStepNdRev, 0),
                        itemsNdRev.style.transform = "translateX(-".concat(currentScrollNdRev, "px)")
                }),
                nextButtonNdRev.addEventListener("click", function () {
                    var e = itemsNdRev.scrollWidth - itemsNdRev.clientWidth;
                    currentScrollNdRev = Math.min(currentScrollNdRev + scrollStepNdRev, e),
                        itemsNdRev.style.transform = "translateX(-".concat(currentScrollNdRev, "px)")
                }),
                itemsNdRev.addEventListener("touchstart", function (e) {
                    startXNdRev = e.touches[0].pageX - itemsNdRev.offsetLeft
                }),
                itemsNdRev.addEventListener("touchend", function (e) {
                    var e = e.changedTouches[0].pageX - itemsNdRev.offsetLeft - startXNdRev;
                    Math.abs(e) > scrollStepNdRev / 4 && (currentScrollNdRev = 0 < e ? Math.max(currentScrollNdRev - scrollStepNdRev, 0) : (e = itemsNdRev.scrollWidth - itemsNdRev.clientWidth,
                        Math.min(currentScrollNdRev + scrollStepNdRev, e)),
                        itemsNdRev.style.transform = "translateX(-".concat(currentScrollNdRev, "px)"))
                })),
        {
            pl: {
                formSent: "Dziękujemy. Twoja wiadomość została wysłana poprawnie.",
                errors: {
                    "Length must be between 1 and 200.": "Długość musi wynosić od 1 do 200 znaków.",
                    "Not a valid email address.": "Niepoprawny adres email.",
                    "Length must be between 1 and 1000.": "Długość musi wynosić od 1 do 1000 znaków.",
                    "Length must be between 1 and 100.": "Długość musi wynosić od 1 do 100 znaków.",
                    "Missing data for required field.": "Brak danych dla wymaganego pola.",
                    "Length must be between 1 and 20.": "Długość musi wynosić od 1 do 20 znaków.",
                    tooManyRequests: "Osiągnąłeś limit wysłanych wiadomości. Spróbuj ponownie później.",
                    errorDefault: "Nie udało wysłać się wiadomości. Spróbuj później."
                }
            },
            en: {
                formSent: "Thank you. Your message has been sent successfully.",
                errors: {
                    "Length must be between 1 and 200.": "Length must be between 1 and 200.",
                    "Not a valid email address.": "Not a valid email address.",
                    "Length must be between 1 and 1000.": "Length must be between 1 and 1000.",
                    "Length must be between 1 and 100.": "Length must be between 1 and 100.",
                    "Missing data for required field.": "Missing data for required field.",
                    "Length must be between 1 and 20.": "Length must be between 1 and 20.",
                    tooManyRequests: "Too many requests. Please try again later.",
                    errorDefault: "An error occurred. Please try again later."
                }
            }
        });
function getTranslation(e) {
    return translations[e] || translations.en
}
var userLang = navigator.language || navigator.userLanguage
    , userLangShort = userLang.split("-")[0]
    , translation = getTranslation(userLangShort);
