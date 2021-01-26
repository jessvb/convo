import { useEffect } from 'react';

const useScript = (path) => {
    useEffect(() => {
      const script = document.createElement('script');
      script.src = path;
      script.async = true;
      document.body.appendChild(script);
      return () => {
        document.body.removeChild(script);
      }
    }, [path]);
  };

export default useScript;