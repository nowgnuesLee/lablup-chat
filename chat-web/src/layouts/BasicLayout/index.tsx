import { Outlet } from "react-router";

const BasicLayout = () => {
  return (
    <main className="overflow-hidden w-dvw h-dvh max-h-dvh">
      <div className="overflow-hidden shadow-lg md:max-w-screen-sm md:mx-auto min-h-dvh h-dvh">
        <Outlet />
      </div>
    </main>
  );
};

export default BasicLayout;
