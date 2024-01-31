<style>
	.navbar-brand {
		font-family:navbar-brand,League Gothic;
		display: flex;
		align-items: center;
		z-index: 1000;
		color: rgb(63, 29, 56);
	}

	.navbar-brand img {
		width: 60px; 
		height: 60px; 
		border-radius: 50%; 
		margin-right: 10px;  /* 調整圖片與文字之間的間距 */
	}
	.navbar-brand b {
		font-size: 35px;
	}

	.navbar.bg-light {
		background-color: #E19898 !important;
	}
	.logo-color {
		color: rgb(63, 29, 56); /*logo*/ 
	}
	.sign-color {
		color: rgb(162, 103, 138); /*logo*/
	}

	.navbar-collapse{
		font-size:20px;
	}

</style>


<nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
	<a class="navbar-brand" href="home.php">
		<img src="image/logo3.jpg" class="d-inline-block align-top img-circle" alt="Logo">
		<b><span class="logo-color">TW</span><span class="sign-color">sign</span><span class="logo-color">Tube</span></b>
	</a>

	<div class="collapse navbar-collapse" id="navbarSupportedContent">
		<div class="mr-auto"></div>
			<ul class="navbar-nav my-2 my-lg-0">
				<li class="nav-item active"><a class="nav-link" href="home.php">Home</a></li>
				<li class="nav-item active"><a class="nav-link" href="about.php">About</a></li>
				<li class="nav-item active"><a class="nav-link" href="search.php">Search</a></li>
			</ul>
	</div>
</nav>