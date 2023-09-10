const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", addToCart);
    });

    function addToCart(event) {
        const adContainer = event.target.closest(".ad-item");
        const adImage = adContainer.querySelector(".ad-image");
        const adTitle = adContainer.querySelector("h3").textContent;
        const adPrice = adContainer.querySelector("p").textContent;

        const cartItem = document.createElement("div");
        cartItem.style.display = "flex";
        cartItem.style.alignItems = "center";
        cartItem.style.marginTop = "10px";
        cartItem.style.padding = "10px";
        cartItem.style.border = "1px solid black";
        cartItem.style.borderRadius = "4px";

        const imageContainer = document.createElement("div");
        imageContainer.style.width = "120px";
        imageContainer.style.height = "120px";
        imageContainer.style.overflow = "hidden";

        const image = document.createElement("img");
        image.style.width = "100%";
        image.style.height = "100%";
        image.style.objectFit = "cover";
        image.src = adImage.src;

        const detailsContainer = document.createElement("div");
        detailsContainer.style.marginLeft = "10px";
        detailsContainer.style.flexGrow = "1";

        const title = document.createElement("h4");
        title.textContent = adTitle;

        const price = document.createElement("p");
        price.style.marginTop = "5px";
        price.textContent = adPrice;

        const checkoutButton = document.createElement("button");
        checkoutButton.textContent = "Оформить заказ";

        const removeButton = document.createElement("button");
        removeButton.textContent = "Удалить из корзины";
        removeButton.style.marginLeft = "10px";

        cartItem.appendChild(imageContainer);
        imageContainer.appendChild(image);

        detailsContainer.appendChild(title);
        detailsContainer.appendChild(price);
        detailsContainer.appendChild(checkoutButton);
        detailsContainer.appendChild(removeButton);

        cartItem.appendChild(detailsContainer);

        document.getElementById("cart-items").appendChild(cartItem);
    }

