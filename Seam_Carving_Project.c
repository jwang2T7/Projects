
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> 
#include <math.h>
struct rgb_img{
    uint8_t *raster;
    size_t height;
    size_t width;
};

void calc_energy(struct rgb_img *im, struct rgb_img **grad);
void dynamic_seam(struct rgb_img *grad, double **best_arr);
void recover_path(double *best, int height, int width, int **path);
void remove_seam(struct rgb_img *src, struct rgb_img **dest, int *path);

void create_img(struct rgb_img **im, size_t height, size_t width);
void read_in_img(struct rgb_img **im, char *filename);
void write_img(struct rgb_img *im, char *filename);
uint8_t get_pixel(struct rgb_img *im, int y, int x, int col);
void set_pixel(struct rgb_img *im, int y, int x, int r, int g, int b);
void destroy_image(struct rgb_img *im);
void print_grad(struct rgb_img *grad);

void calc_energy(struct rgb_img *im, struct rgb_img **grad){
    create_img(grad,im->height,im->width);
    for(int i=0; i<im->height;i++){
        for(int k=0; k<im->width;k++){
            double rx, gx, bx, ry, gy, by;
            int xtrue=0;
            int ytrue=0;
            //check edge for row
            //printf("coordinate: %d, %d\n",k,i);
            if(i==0){
                ry=(double)get_pixel(im,i+1,k,0)-(double)get_pixel(im,im->height-1,k,0);
                gy=(double)get_pixel(im,i+1,k,1)-(double)get_pixel(im,im->height-1,k,1);
                by=(double)get_pixel(im,i+1,k,2)-(double)get_pixel(im,im->height-1,k,2);
                ytrue=1;
                //printf("(i=0) ry: %f, gy: %f, by: %f\n",ry,gy,by);
            }
            if(i==im->height-1){
                ry=(double)get_pixel(im,i-1,k,0)-(double)get_pixel(im,0,k,0);
                gy=(double)get_pixel(im,i-1,k,1)-(double)get_pixel(im,0,k,1);
                by=(double)get_pixel(im,i-1,k,2)-(double)get_pixel(im,0,k,2);
                ytrue=1;
                //printf("(i=height-1) ry: %f, gy: %f, by: %f\n",ry,gy,by);
            }
            //check edge for col
            if(k==0){
                rx=(double)get_pixel(im,i,k+1,0)-(double)get_pixel(im,i,im->width-1,0);
                gx=(double)get_pixel(im,i,k+1,1)-(double)get_pixel(im,i,im->width-1,1);
                bx=(double)get_pixel(im,i,k+1,2)-(double)get_pixel(im,i,im->width-1,2);
                xtrue=1;
                //printf("(k=0) rx: %f, gx: %f, bx: %f\n",rx,gx,bx);
            }
            if(k==im->width-1){
                rx=(double)get_pixel(im,i,k-1,0)-(double)get_pixel(im,i,0,0);
                gx=(double)get_pixel(im,i,k-1,1)-(double)get_pixel(im,i,0,1);
                bx=(double)get_pixel(im,i,k-1,2)-(double)get_pixel(im,i,0,2);
                xtrue=1;
                //printf("(k=width-1) rx: %f, gx: %f, bx: %f\n",rx,gx,bx);
            }
            if(xtrue==0) {
                rx=(double)get_pixel(im,i,k+1,0)-(double)get_pixel(im,i,k-1,0);
                gx=(double)get_pixel(im,i,k+1,1)-(double)get_pixel(im,i,k-1,1);
                bx=(double)get_pixel(im,i,k+1,2)-(double)get_pixel(im,i,k-1,2);
                //printf("(normal) ry: %f, gy: %f, by: %f\n",ry,gy,by);
                //printf("(normal) rx: %f, gx: %f, bx: %f\n",rx,gx,bx);
                }
            if(ytrue==0){
                ry=(double)get_pixel(im,i+1,k,0)-(double)get_pixel(im,i-1,k,0);
                gy=(double)get_pixel(im,i+1,k,1)-(double)get_pixel(im,i-1,k,1);
                by=(double)get_pixel(im,i+1,k,2)-(double)get_pixel(im,i-1,k,2);
            }
            double energy = sqrt(rx * rx + gx * gx + bx * bx + ry * ry + gy * gy + by * by) / 10.0;
            //printf("energy: %f\n",energy);
            uint8_t energ=(uint8_t)energy;
            set_pixel(*grad,i,k,energ,energ,energ);
        }
    }
    
}

void dynamic_seam(struct rgb_img *grad, double **best_arr) {
    *best_arr=(double *)malloc(grad->height * grad->width * sizeof(double));
    
    for(int i=0; i<grad->width;i++){
        (*best_arr)[i]=(double)get_pixel(grad,0,i,0);
    }
    for(int i=1; i<grad->height;i++){
        for(int j=0; j<grad->width;j++){
            double upleft, up, upright;
            if(j==0){
                upleft=INFINITY;
                up=(*best_arr)[(i-1)*grad->width+j];
                upright=(*best_arr)[(i-1)*grad->width+j+1];
            }
            else if(j==grad->width-1){
                upleft=(*best_arr)[(i-1)*grad->width+j-1];
                up=(*best_arr)[(i-1)*grad->width+j];
                upright=INFINITY;
            }
            else {
                upleft=(*best_arr)[(i-1)*grad->width+j-1];
                up=(*best_arr)[(i-1)*grad->width+j];
                upright=(*best_arr)[(i-1)*grad->width+j+1];
            }
            double between;
            if(up<upleft){
                between=up;
            }
            else{
                between=upleft;
            }
            (*best_arr)[i*grad->width+j]=fmin(between,upright)+(double)get_pixel(grad,i,j,0);
        }

    }
        
}

void recover_path(double *best, int height, int width, int **path) {
    *path=(int *)malloc(height * sizeof(int));
    double finval=best[(height-1)*width];
    int curindex=0;
    for(int i=1;i<width;i++){
        if (best[(height-1)*width+i]<finval){
            curindex=i;
            finval=best[(height-1)*width+i];
        }
    }
    (*path)[height-1]=curindex;
    for(int i=height-2;i>=0;i--){
        double upleft, up, upright;
        if(curindex==0){
            upleft=INFINITY;
            up=best[i*width+curindex];
            upright=best[i*width+curindex+1];
        }
        else if(curindex==width-1){
            upleft=best[i*width+curindex-1];
            up=best[i*width+curindex];
            upright=INFINITY;
        }
        else {
            upleft=best[i*width+curindex-1];
            up=best[i*width+curindex];
            upright=best[i*width+curindex+1];
        }
        double between;
        if(up<upleft){
            between=up;
        }
        else{
            between=upleft;
        }
        if(fmin(between,upright)==up){
            curindex=curindex;
        }
        else if(fmin(between,upright)==upleft){
            curindex=curindex-1;
        }
        else{
            curindex=curindex+1;
        }
        (*path)[i]=curindex;
    }

}

void remove_seam(struct rgb_img *src, struct rgb_img **dest, int *path){
    create_img(dest, src->height, src->width-1);
    for(int i = 0; i < src->height; i++){
        for(int j = 0, dest_col = 0; j < src->width; j++){
            if (j != path[i]){
                set_pixel(*dest, i, dest_col, get_pixel(src, i, j, 0), 
                                              get_pixel(src, i, j, 1), 
                                              get_pixel(src, i, j, 2));
                dest_col++; 
            }
        }
    }
}
