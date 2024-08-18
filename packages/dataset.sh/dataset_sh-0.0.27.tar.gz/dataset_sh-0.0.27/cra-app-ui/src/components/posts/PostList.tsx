export function PostListViewer(
    {
        posts

    }: {
        posts: { name: string, mtime: string }[]
    }) {

    return <>
        {posts.map(x => {
            return <>
                
            </>
        })}
    </>

}