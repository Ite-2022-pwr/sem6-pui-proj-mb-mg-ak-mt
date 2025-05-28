import Navbar from "../components/Navbar";

function BrowseMovies() {
  return (
    <>
      <Navbar />
      <div className="bg-mywhite min-h-screen px-8 py-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-mydarkblue text-3xl font-limelight border-b w-fit">
            Browse movies
          </h2>
          <input
            type="text"
            placeholder="Search"
            className="rounded-full px-4 py-1 bg-myyellow-1 text-mydarkblue placeholder-mydarkblue focus:outline-none w-48"
          />
        </div>
      </div>
    </>
  );
}

export default BrowseMovies;
