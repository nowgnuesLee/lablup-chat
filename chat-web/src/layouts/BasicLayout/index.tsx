import { Outlet } from "react-router";
const BasicLayout = () => {
  return (
    <main className="overflow-hidden w-dvw h-dvh max-h-dvh">
      <div className="flex justify-around overflow-hidden min-h-dvh h-dvh">
        <div className="hidden w-full lg:flex md:max-w-screen-md">
          <img
            src="/logo.png"
            className="object-contain w-full h-full"
            alt="lablup"
          />
        </div>
        <div className="w-full shadow-2xl md:max-w-screen-md">
          <Outlet />
        </div>
      </div>
    </main>
  );
};

export default BasicLayout;
